% rebase('base.tpl', title='Medojed - Search')

<div class="template">
    <h1>Search</h1>
</div>

%def render_field(field, desc=None, **kwargs):
<div class="form-group">
    {{!field.label(class_="col-sm-2 form-control-label")}}
    <div class="col-sm-10">
        {{!field(class_="form-control")}}
    </div>
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
        %render_field(form.request)
        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10 ">
                <input type="submit" class="btn btn-default" value="Search!">
            </div>
        </div>
    </form>
</div>
