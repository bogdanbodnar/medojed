% rebase('base.tpl', title='Medojed - Pages')
<div class="template">
    <form action="/pages/rank">
    <input class="btn btn-primary"  type="submit" value="Rank!">
</form>
</div>
<p>
%for page in pages:
<p><b>URL:</b><a href={{page.url}}> {{page.url}} </a><p>
<p><b>Rank:</b> {{page.rank}}</p>
<br>

