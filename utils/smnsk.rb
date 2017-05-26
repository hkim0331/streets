#!/usr/bin/env ruby
# coding: utf-8
index = "/srv/streets/public/index.html"

def bootstrap(title)
  ret = <<EOH
<html>
<head>
<meta charset='utf-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
      rel="stylesheet">
<style>
img.home { width: 64px;}
</style>
<title>#{title}</title>
</head>
<body>
<div class="container">
EOH
end

def redirect(where, bootstrap)
  bootstrap.sub(/<head>/,
                "<head><meta http-equiv='refresh' content='1;#{where}'>")
end

def space()
  puts "<div class='col-md-1'></div>"
end

def home(sid)
  unless File.exists?(File.join(sid,"home.gif"))
    system("cp home.gif #{sid}")
  end
  ret =<<EOH
<div class='col-md-2'>
<a href="/#{sid}/"><img class='home' src="/#{sid}/home.gif"></a>
</div>
EOH
end

#
# main starts here
#

students = Array.new
File.foreach("smnsk.txt") do |line|
  next if line =~ /^\s*$/
  students.push line.chomp
end

puts bootstrap("下関11/12組のまち")
puts "<h1>下関11/12組のまち</h1>"

MOD = 5
n = 0
students.each do |sid|
  n += 1
  Dir.mkdir sid unless Dir.exists? sid
  if n.to_i % MOD == 1
    puts "<div class='row'>"
    space()
  end
  puts home(sid)
  if n.to_i % MOD == 0
    space()
    puts "</div>"
  end
end
2.times do
  space()
end
puts "</div>"

print <<EOF
<hr>
管理人 <a href="/123456/"><img class='home' src="/123456/home.gif"></a>
</div></body></html>
EOF
