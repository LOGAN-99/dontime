/**
 * 셈플리 랭킹 API (Google Apps Script)
 * Spreadsheet: 1JcC8yaeMfcqes8mdpuyO0_pK4tp_5LB3A8P0BEOzhsQ
 * Sheet: 셈플리_게임기록
 *
 * 배포 전:
 * 1) 이 코드를 기존 Apps Script 프로젝트의 Code.gs에 붙여넣습니다.
 * 2) setupSempliRanking()을 한 번 직접 실행하고 권한을 승인합니다.
 * 3) 배포 > 배포 관리 > 기존 웹 앱 배포 수정 > 새 버전 선택
 * 4) 실행 사용자: 나 / 액세스 권한: 모든 사용자
 * 5) HTML의 SEMPLI_RANKING_API URL이 이 배포 URL과 같은지 확인합니다.
 */
const SPREADSHEET_ID = '1JcC8yaeMfcqes8mdpuyO0_pK4tp_5LB3A8P0BEOzhsQ';
const SHEET_NAME = '셈플리_게임기록';
const HEADERS = [
  '기록 ID', '카테고리', '게임 ID', '닉네임', '경과 시간(초)',
  '점수', '기록 유형', '기록 시각(ISO)', '검증 상태', '비고'
];

function setupSempliRanking() {
  const sheet = getOrCreateSheet_();
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  return '셈플리 랭킹 시트 준비 완료: ' + sheet.getName();
}

function doGet(e) {
  try {
    const params = (e && e.parameter) || {};
    const action = String(params.action || '');
    if (action === 'health') {
      const sheet = getOrCreateSheet_();
      return json_({ ok: true, sheet: sheet.getName(), rows: Math.max(0, sheet.getLastRow() - 1) });
    }
    if (action !== 'leaderboard') {
      return json_({ ok: false, error: 'Unknown action. Use action=leaderboard or action=health.' });
    }

    const category = String(params.category || '').trim();
    const gameId = String(params.gameId || '').trim();
    const limit = Math.min(50, Math.max(1, parseInt(params.limit || '10', 10) || 10));
    const sheet = getOrCreateSheet_();
    ensureHeaders_(sheet);

    const lastRow = sheet.getLastRow();
    if (lastRow < 2) return json_({ ok: true, records: [] });

    const rows = sheet.getRange(2, 1, lastRow - 1, HEADERS.length).getValues();
    const records = rows
      .filter(row => String(row[1]).trim() === category && String(row[2]).trim() === gameId)
      .map(row => ({
        id: String(row[0] || ''),
        category: String(row[1] || ''),
        gameId: String(row[2] || ''),
        nickname: String(row[3] || '익명'),
        elapsedSeconds: Math.max(0, Number(row[4]) || 0),
        score: Number(row[5]) || 0,
        recordType: String(row[6] || ''),
        createdAt: String(row[7] || ''),
        verificationStatus: String(row[8] || '')
      }))
      .sort((a, b) => (b.score - a.score) || (a.elapsedSeconds - b.elapsedSeconds))
      .slice(0, limit);

    return json_({ ok: true, records: records });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  }
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const raw = e && e.postData && e.postData.contents;
    if (!raw) return json_({ ok: false, error: 'Empty request body.' });

    const data = JSON.parse(raw);
    const category = String(data.category || '').trim();
    const gameId = String(data.gameId || '').trim();
    const nickname = String(data.nickname || '').trim().slice(0, 20);
    const elapsedSeconds = Math.floor(Number(data.elapsedSeconds));
    const score = Math.floor(Number(data.score));

    if (!category || !gameId) return json_({ ok: false, error: 'category and gameId are required.' });
    if (!nickname) return json_({ ok: false, error: 'nickname is required.' });
    if (!Number.isFinite(elapsedSeconds) || elapsedSeconds < 0) return json_({ ok: false, error: 'Invalid elapsedSeconds.' });
    if (!Number.isFinite(score) || score < 0) return json_({ ok: false, error: 'Invalid score.' });

    const sheet = getOrCreateSheet_();
    ensureHeaders_(sheet);
    const now = new Date();
    const record = [
      Utilities.getUuid(),
      category,
      gameId,
      nickname,
      elapsedSeconds,
      score,
      '게임완료',
      now.toISOString(),
      '검증 전',
      '웹 앱 제출'
    ];
    sheet.appendRow(record);

    return json_({ ok: true, record: {
      id: record[0], category: category, gameId: gameId, nickname: nickname,
      elapsedSeconds: elapsedSeconds, score: score, createdAt: record[7],
      verificationStatus: record[8]
    }});
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  } finally {
    try { lock.releaseLock(); } catch (ignored) {}
  }
}

function getOrCreateSheet_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  ensureHeaders_(sheet);
  return sheet;
}

function ensureHeaders_(sheet) {
  const current = sheet.getRange(1, 1, 1, HEADERS.length).getDisplayValues()[0];
  const same = HEADERS.every((header, i) => String(current[i] || '').trim() === header);
  if (!same) {
    // Only normalize the header row. Existing data rows are retained.
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
  }
}

function json_(value) {
  return ContentService
    .createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}
