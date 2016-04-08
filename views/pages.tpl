% rebase('base.tpl', title='Medojed - Pages')
<div class="template">
    <form action="/pages/remove">
    <input class="btn btn-danger"  type="submit" value="Remove all pages!">
</form>
</div>
%for page in pages:
<p><b>URL:</b><a href=http://{{page.url}}> {{page.url}} </a><p>
<p><b>Rank:</b> {{page.rank}}</p>
<br>

