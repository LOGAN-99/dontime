<?php
$tool=$_GET['tool']??'income';
$services=['income'=>['월급시계','월급을 시간과 초 단위로 바꿔 실시간으로 확인합니다.'],'hourly'=>['시급 계산','월급과 근무시간으로 한 시간의 가치를 계산합니다.'],'salary'=>['연봉 월급 계산','연봉과 월급을 서로 바꿔 계산합니다.']];
$s=$services[$tool]??$services['income'];
$title=$s[0].' 계산기 | 돈시간';
$desc='돈시간 '.$s[0].' 계산기입니다. '.$s[1];
$canonical='https://dontime.kr/calculator.php?tool='.rawurlencode($tool);
function h($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
?><!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><meta name="description" content="<?=h($desc)?>"><link rel="canonical" href="<?=h($canonical)?>"><title><?=h($title)?></title></head><body><main><nav><a href="/">돈시간</a> › 계산기</nav><h1><?=h($s[0])?> 계산기</h1><p><?=h($s[1])?></p><a href="/?tool=<?=rawurlencode($tool)?>">계산기 바로 사용하기</a></main></body></html>