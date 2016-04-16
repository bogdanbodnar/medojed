% rebase('base.tpl', title='Medojed - Crawler')
<div class="template">
    <h1>Crawler</h1>
</div>
%def render_field(field, desc=None, **kwargs):
<div class="form-group row">
    %if field.type == "StringField" or field.type == "IntegerField":
    {{!field.label(class_="col-sm-2 form-control-label")}}
    <div class="col-sm-10">
        {{!field(class_="form-control")}}
    </div>
    %end

    %if field.type == "BooleanField":
    {{!field.label(class_="col-sm-2")}}
    <div class="col-sm-10">
        <div class="checkbox">
            <label>{{!field}}</label>
        </div>
    </div>
    %end

    %if desc:
    {{!desc}}
    %end
    %if field.errors:
    <ul class=errors>
        %for error in field.errors:
        {{ error }}
        %end
    </ul>
    %end
</div>
%end

<div class="container">
    <form class="form-horizontal" role="form" method="POST">
        %render_field(form.url)
        %render_field(form.depth)
        %render_field(form.threads)
        %render_field(form.max_pages)
        %render_field(form.uel)
        <div class="form-group row">
            <div class="col-sm-offset-2 col-sm-10">
                <input type=submit class="btn btn-default" value="Crawl!">
            </div>
        </div>
    </form>
</div>