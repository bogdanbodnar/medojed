% include('search.tpl')

%for page in pages:
<p><b>URL:</b><a href=http://{{page.url}}> {{page.url}} </a><p>
<p><b>Rank:</b> {{page.rank}}</p>
<br>
