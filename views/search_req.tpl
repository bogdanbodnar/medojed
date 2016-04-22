% include('search.tpl')
<div class="container">
    %if total_pages == 0:
    <p>Nothing found</p>
    %else:
    <p style="color:gray">About {{total_pages}} results ({{"%.3f" % total_time}} seconds) </p>
    <br>
    % include('page_view.tpl')
    %include('pagination.tpl', link = "search/"+s_req)

    <br>
</div>