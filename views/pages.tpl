<button  class="btn btn-default" type="button"><a href="/pages/remove">Remove all pages!</a></button>
<br>

% rebase('base.tpl', title='Medojed - Crawler')
%for page in pages:
    <p><b>URL:</b><a href = http://{{page.url}}> {{page.url}} </a><p>
    <p><b>Rank:</b> {{page.rank}}</p>
    <br>

