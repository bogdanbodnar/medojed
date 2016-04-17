<ul class="pagination">
    %for i in range(1, int(total_pages/pages_to_display)+2):
        %if current_page == i:
            <li class="active"><a href="/{{link}}/{{i}}">{{i}}</a></li>
        %elif i == 1 or i == (int(total_pages/pages_to_display) + 1) or (i < current_page+5 and i > current_page-5):
            <li><a href="/{{link}}/{{i}}">{{i}}</a></li>
        %end
    %end
</ul>