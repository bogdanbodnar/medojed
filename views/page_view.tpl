%for page in pages:
<p><b><a href={{page.url}}> <font color="#1A0DAB">{{page.text.split("\n")[0]}} </font> </a></b><p>
<p><a href={{page.url}}> <font color="#006621">{{page.url}} </font></a><p>
<p><b>Rank:</b> {{page.rank}}</p>
<br>
%end