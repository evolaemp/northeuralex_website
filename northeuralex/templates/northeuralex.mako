<%inherit file="app.mako"/>

<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">NorthEuraLex</a>
</%block>

<%block name="footer">
    <div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
        <div class="span3">
            <a href="http://www.evolaemp.uni-tuebingen.de/" title="Project EVOLAEMP">
                <img src="http://www.evolaemp.uni-tuebingen.de/img/logo.png" />
            </a>
        </div>
        <div class="span6" style="text-align: center;">
            <% license_icon = h.format_license_icon_url(request) %>
            % if license_icon:
            <a rel="license" href="${request.dataset.license}">
                <img alt="License" style="border-width:0" src="${license_icon}" />
            </a>
            <br />
            % endif
            ${request.dataset.formatted_name()}
            edited by
            <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName" rel="cc:attributionURL">${request.dataset.formatted_editors()}</span>
            is licensed under a
            <a rel="license" href="${request.dataset.license}">${request.dataset.jsondata.get('license_name', request.dataset.license)}</a>.
            This research has been supported by the ERC Advanced Grant 324246 EVOLAEMP, which is gratefully acknowledged.
        </div>
        <div class="span3" style="text-align: right;">
            <a href="${request.route_url('legal')}">disclaimer</a>
            <br/>
            % if request.registry.settings.get('clld.github_repos'):
            <a href="https://github.com/${request.registry.settings['clld.github_repos']}">
                <i class="icon-share">&nbsp;</i>
                Application source on<br/>
                <img height="25" src="${request.static_url('clld:web/static/images/GitHub_Logo.png')}" />
            </a>
            % endif
        </div>
    </div>
</%block>

${next.body()}
