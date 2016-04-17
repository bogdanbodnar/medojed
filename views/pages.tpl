% rebase('base.tpl', title='Medojed - Pages')
<div class="template">
    <form action="/pages/rank">
    <input class="btn btn-primary"  type="submit" value="Rank!">
</form>
</div>

% include('page_view.tpl')

<ul class="pagination">
    %print(num)
    %for i in range(1, int(total_pages/on_page)+2):
        %if int(num) == i:
            <li class="active"><a href="/pages/{{i}}">{{i}}</a></li>
        %elif i == 1 or i == (int(total_pages/on_page) + 1) or (i < int(num)+5 and i > int(num)-5):
            <li><a href="/pages/{{i}}">{{i}}</a></li>
        %end
    %end
</ul>
<br>