<?php
declare(strict_types=1);
$now = new DateTimeImmutable('now');
$year = isset($_GET['year']) ? (int)$_GET['year'] : $now->format('Y') + 1;
$month = isset($_GET['month']) ? (int)$_GET['month'] : 5;
$year = max(1027, min((int)$now->format('Y') + 100, $year));
$month = max(1, min(12, $month));

$monthNames = [1=>'1월',2=>'2월',3=>'3월',4=>'4월',5=>'5월',6=>'6월',7=>'7월',8=>'8월',9=>'9월',10=>'10월',11=>'11월',12=>'12월'];
$weekNames = ['일','월','화','수','목','금','토'];

$holidays = [
  2027 => [
    '01-01'=>'신정','02-06'=>'설날 연휴','02-07'=>'설날','02-08'=>'설날 연휴',
    '03-01'=>'삼일절','05-05'=>'어린이날 · 부처님오신날','05-13'=>'부처님오신날',
    '06-06'=>'현충일','08-15'=>'광복절','09-14'=>'추석 연휴','09-15'=>'추석','09-16'=>'추석 연휴',
    '10-03'=>'개천절','10-09'=>'한글날','12-25'=>'성탄절'
  ]
];
$holidayMap = $holidays[$year] ?? [];
$first = new DateTimeImmutable(sprintf('%04d-%02d-01', $year, $month));
$daysInMonth = (int)$first->format('t');
$firstDow = (int)$first->format('w');
$title = sprintf('%d년 %d월 달력 | 공휴일·요일 확인 | 돈시간', $year, $month);
$desc = sprintf('%d년 %d월 달력입니다. %d년 %s의 날짜, 요일, 토요일·일요일과 확인 가능한 공휴일을 한눈에 확인하세요.', $year, $month, $year, $monthNames[$month]);
$canonical = 'https://dontime.kr/calendar.php?year='.$year.'&month='.$month;
function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }
$prev = $first->modify('-1 month'); $next = $first->modify('+1 month');
$isNextYear = ((int)$now->format('Y') + 1 === $year);
$holidayCount = 0; $sat = 0; $sun = 0; $weekday = 0;
for($d=1;$d<=$daysInMonth;$d++){ $dt=$first->modify('+'.($d-1).' days'); $dow=(int)$dt->format('w'); if($dow===0)$sun++; elseif($dow===6)$sat++; else $weekday++; $key=$dt->format('m-d'); if(isset($holidayMap[$key]))$holidayCount++; }
?>
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow">
<meta name="description" content="<?=h($desc)?>">
<link rel="canonical" href="<?=h($canonical)?>">
<meta property="og:type" content="website">
<meta property="og:site_name" content="돈시간">
<meta property="og:title" content="<?=h($title)?>">
<meta property="og:description" content="<?=h($desc)?>">
<meta property="og:url" content="<?=h($canonical)?>">
<meta property="og:locale" content="ko_KR">
<title><?=h($title)?></title>
<script type="application/ld+json"><?=json_encode([
  '@context'=>'https://schema.org','@type'=>'WebPage','name'=>$title,'url'=>$canonical,'description'=>$desc,'inLanguage'=>'ko-KR'
], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<script type="application/ld+json"><?=json_encode([
  '@context'=>'https://schema.org','@type'=>'BreadcrumbList','itemListElement'=>[
    ['@type'=>'ListItem','position'=>1,'name'=>'돈시간','item'=>'https://dontime.kr/'],
    ['@type'=>'ListItem','position'=>2,'name'=>'달력','item'=>'https://dontime.kr/calendar.php'],
    ['@type'=>'ListItem','position'=>3,'name'=>$year.'년 '.$monthNames[$month].' 달력','item'=>$canonical]
  ]
], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<style>
*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#17191c;font-family:Arial,"Noto Sans KR",sans-serif}
.wrap{max-width:980px;margin:auto;padding:28px 18px 60px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}.logo{font-size:24px;font-weight:900}.home{color:#666;text-decoration:none;font-size:13px}
.breadcrumb{font-size:12px;color:#777;margin-bottom:16px}.breadcrumb a{color:#666}.hero{background:#fff;border:1px solid #e2e5e9;border-radius:18px;padding:24px;margin-bottom:16px}.hero h1{font-size:30px;margin:0 0 9px;letter-spacing:-1px}.hero p{margin:0;color:#666;line-height:1.7;font-size:14px}
.month-nav{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:14px 0}.month-nav a{padding:9px 12px;background:#fff;border:1px solid #dfe3e8;border-radius:9px;color:#333;text-decoration:none;font-size:12px;font-weight:800}.month-nav strong{font-size:18px}
.calendar{background:#fff;border:1px solid #dfe3e8;border-radius:18px;padding:14px}.week,.days{display:grid;grid-template-columns:repeat(7,1fr);gap:5px}.week div{text-align:center;color:#777;font-size:12px;font-weight:800;padding:8px 0}.day{min-height:92px;border:1px solid #edf0f2;border-radius:10px;padding:8px;background:#fff}.day.empty{background:#fafbfc}.day .num{font-size:14px;font-weight:800}.day.sun,.day.holiday{color:#c84a4a}.day.sat{color:#4f6f99}.holiday-name{display:block;font-size:10px;line-height:1.35;margin-top:8px}.today{box-shadow:inset 0 0 0 2px #17191c}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:14px}.stat{background:#fff;border:1px solid #e2e5e9;border-radius:12px;padding:13px;text-align:center}.stat strong{display:block;font-size:20px}.stat span{font-size:11px;color:#777}
.info{background:#fff;border:1px solid #e2e5e9;border-radius:16px;padding:20px;margin-top:16px}.info h2{font-size:18px;margin:0 0 9px}.info p{font-size:13px;line-height:1.75;color:#555}.links{display:flex;flex-wrap:wrap;gap:7px}.links a{padding:7px 9px;background:#f4f5f7;border-radius:8px;color:#555;text-decoration:none;font-size:11px}
footer{margin-top:30px;padding-top:18px;border-top:1px solid #ddd;color:#888;font-size:12px}footer a{color:#666;margin-right:12px}
@media(max-width:650px){.wrap{padding:20px 12px 45px}.hero h1{font-size:25px}.day{min-height:64px;padding:6px}.holiday-name{font-size:8px;margin-top:5px}.stats{grid-template-columns:1fr 1fr}.month-nav strong{font-size:16px}}
</style>
</head>
<body>
<main class="wrap">
  <div class="top"><div class="logo">돈시간</div><a class="home" href="/">← 돈시간 계산기</a></div>
  <nav class="breadcrumb" aria-label="사이트 이동 경로"><a href="/">돈시간</a> › <a href="calendar.php">달력</a> › <span><?=h($year.'년 '.$monthNames[$month])?></span></nav>
  <section class="hero">
    <h1><?=h($year.'년 '.$monthNames[$month])?> 달력</h1>
    <p><?=h($year.'년 '.$monthNames[$month])?>의 날짜와 요일을 확인하세요. 토요일·일요일을 구분하고, 제공 가능한 공휴일 정보도 함께 표시합니다.<?= $isNextYear ? ' 현재 기준 내년 달력을 찾는 분도 바로 확인할 수 있습니다.' : '' ?></p>
  </section>
  <div class="month-nav">
    <a href="calendar.php?year=<?=$prev->format('Y')?>&month=<?=$prev->format('n')?>">‹ 이전 달</a>
    <strong><?=h($year.'년 '.$monthNames[$month])?></strong>
    <a href="calendar.php?year=<?=$next->format('Y')?>&month=<?=$next->format('n')?>">다음 달 ›</a>
  </div>
  <section class="calendar" aria-label="<?=h($year.'년 '.$monthNames[$month])?> 달력">
    <div class="week"><?php foreach($weekNames as $w): ?><div><?=$w?></div><?php endforeach; ?></div>
    <div class="days">
    <?php for($i=0;$i<$firstDow;$i++): ?><div class="day empty" aria-hidden="true"></div><?php endfor; ?>
    <?php for($d=1;$d<=$daysInMonth;$d++):
      $dt=$first->modify('+'.($d-1).' days'); $dow=(int)$dt->format('w'); $key=$dt->format('m-d'); $isHoliday=isset($holidayMap[$key]); $cls='day '.($dow===0?'sun ':($dow===6?'sat ':'')).($isHoliday?'holiday ':''); $isToday=$dt->format('Y-m-d')===$now->format('Y-m-d'); if($isToday)$cls.='today';
    ?>
      <div class="<?=trim($cls)?>">
        <span class="num"><?=$d?></span>
        <?php if($isHoliday): ?><span class="holiday-name"><?=h($holidayMap[$key])?></span><?php endif; ?>
      </div>
    <?php endfor; ?>
    </div>
  </section>
  <div class="stats">
    <div class="stat"><strong><?=$holidayCount?>일</strong><span>표시된 공휴일</span></div>
    <div class="stat"><strong><?=$sat?>일</strong><span>토요일</span></div>
    <div class="stat"><strong><?=$sun?>일</strong><span>일요일</span></div>
    <div class="stat"><strong><?=$weekday?>일</strong><span>평일</span></div>
  </div>
  <section class="info">
    <h2><?=h($year.'년 '.$monthNames[$month])?> 공휴일과 달력</h2>
    <p>돈시간 달력은 선택한 연도와 월의 날짜 및 요일을 계산해서 보여줍니다. 한국 공휴일 이름은 확인 가능한 연도에 한해 표시하며, 데이터가 없는 연도는 공휴일을 임의로 확정하지 않습니다.</p>
    <h2>다른 달 보기</h2>
    <div class="links"><?php for($m=1;$m<=12;$m++): ?><a href="calendar.php?year=<?=$year?>&month=<?=$m?>"><?=$year?>년 <?=$monthNames[$m]?></a><?php endfor; ?></div>
  </section>
  <footer>돈시간 · <a href="/">생활 계산기</a><a href="about.html">서비스 안내</a><a href="privacy.html">개인정보처리방침</a><a href="terms.html">이용약관</a><a href="contact.html">문의</a></footer>
</main>
</body>
</html>
