#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'logger'

if File.exists?("/srv/streets/public")
  UPLOAD = "/srv/streets/public"
else
  UPLOAD = "../public"
end

if File.exists?("/srv/streets/log")
  LOG = "/srv/streets/log/streets.log"
else
  LOG = "../log/streets.log"
end

def index()
  print <<EOF
<form method='post' enctype='multipart/form-data'
  style='border:dotted 1pt; padding:10px;'>
<p>学生番号 <input name="sid">半角数字</p>
<p>ファイル <input class='btn' name="file" type="file"></p>
<p>save as <input name="save_as">日本語ファイル名は不可、拡張子を変えないように。
カラの時は選んだファイルと同じ名前。  </p>
<p><input class='btn btn-primary' type="submit" value="アップロード"></p>
</form>

<ul>
<li>まち図の家の絵は home.gif</li>
<li>自分の家の内容は index.html</li>
<li>自分ちのホームページに絵を貼り込むときは
index.html にその絵のファイル名をプログラムし、
index.html と絵のファイルを忘れずにアップロード。</li>
</ul>
EOF
end

def upload(cgi)
  sid = cgi['sid'].read
  original_filename = cgi['file'].original_filename
  save_as = cgi['save_as'].read
  save_as = original_filename if save_as.empty?

  # log 100KB max, rotate five old files.
  log = Logger.new(LOG, 5, 100*1024)
  log.level = Logger::DEBUG
  log.info("from #{cgi.remote_addr}, sid #{sid}, original #{original_filename}, save_as #{save_as}")

  raise "学生番号を入力してください。" if sid.empty?
  raise "学生番号を確認してください。" unless sid =~ /\d{6}/
  raise "ファイルが選ばれていません。" if original_filename.empty?
  raise "ファイルが大きすぎます。最大は 500KB です。" if cgi['file'].size > 500*1014

  Dir.mkdir("#{UPLOAD}/#{sid}") unless Dir.exists?("#{UPLOAD}/#{sid}")
  File.open("#{UPLOAD}/#{sid}/#{save_as}", "w") do |fp|
    cgi['file'].readlines.each do |line|
      fp.puts line
    end
  end
  print <<EOM
<p>アップロードできました。&rArr;
<a href="http://streets.melt.kyutech.ac.jp/#{sid}/#{save_as}"</a>
http://streets.melt.kyutech.ac.jp/#{sid}/#{save_as}</p>
EOM
end

#
# main
#
cgi = CGI.new

print <<EOH
content-type: text/html

<!DOCTYPE html>
<html>
<head>
  <meta http-equiv='X-UA-Compatible' content='IE=edge' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta name="generator" content="pandoc" />
  <title>streets</title>
  <style type="text/css">
    code {white-space: pre;}
    .group {border:dotted 1pt; padding:10px;}
  </style>
  <link rel="stylesheet"
   href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
<div class="container">
<h1>UPLOAD</h1>
EOH

begin

  if cgi.request_method =~ /GET/
    index()
  elsif cgi.request_method =~ /POST/
    upload(cgi)
  end

rescue
  print <<EOR
<p style='color:red;'>#{$!}</p>
<p>やり直すにはブラウザの「戻る」ボタンで</p>
EOR

ensure
  print <<EOF
<p>
<a href="/cgi/streets.cgi">back</a>
</p>
<hr>
hkimura, 2017-05-22.
</div>
</body>
EOF
end
