%for page in pages:
    %if page.text.split("\n")[0]:
        <p style="margin-bottom:0.1em"><b><a href={{page.url}}> <font color="#1A0DAB">{{page.text.split("\n")[0]}} </font> </a></b></p>
    %else:
        <p style="margin-bottom:0.1em"><b><a href={{page.url}}> <font color=silver> &lt;Content was not crawled&gt; </font> </a></b></p>
    %end
<p><a href={{page.url}}> <font color="#006621">{{page.url}} </font></a></p>
<p><b>Rank:</b> {{page.rank}}</p>
<br>
%end