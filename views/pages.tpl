% rebase('base.tpl', title='Medojed - Pages')
<div class="template">
    <form action="/pages/rank">
    <input class="btn btn-primary"  type="submit" value="Rank!">
</form>
</div>

% include('page_view.tpl')

% include('pagination.tpl', link = "pages")

<br>