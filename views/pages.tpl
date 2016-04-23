% rebase('base.tpl', title='Medojed - Pages')
<!--<div class="template">-->
    <!--<form action="/pages/rank">-->
    <!--<input class="btn btn-primary"  type="submit" value="Rank!">-->
<!--</form>-->
<!--</div>-->


%def render_field(field, desc=None, **kwargs):
<div class="form-group row">
    %if field.type == "StringField" or field.type == "IntegerField" or field.type == "FloatField":
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

    %if field.type == "RadioField":
    <!--{{!field.label(class_="col-sm-2")}}-->
    <div class="col-sm-offset-2">
        <div class="radio" align="left">
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

<div class="template">
<div class="container">
    <form class="form-horizontal" role="form" action="/pages/rank" method="POST">
        %render_field(form.alpha)
        %render_field(form.iterations)
        %render_field(form.choice_switcher)
        <div class="form-group row">
            <div class="col-sm-offset-1 col-sm-10">
                <input class="btn btn-primary"  type="submit" value="Rank!">
            </div>
        </div>
    </form>
</div>
    </div>



% include('page_view.tpl')

% include('pagination.tpl', link = "pages")

<br>