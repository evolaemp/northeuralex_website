<%inherit file="home_comp.mako"/>

<h3>Contact ${h.contactmail(req)}</h3>
<div class="well">
    <p>You can contact us via email at <a href="mailto:${request.dataset.contact}">${request.dataset.contact}</a>.</p>
    <% srepo = request.registry.settings['clld.github_repos'] %>
    <p><a href="https://github.com">GitHub</a> users can also create and discuss bug reports using the following <strong>issue trackers</strong>:</p>
    <ul>
        <li><a href="https://github.com/${srepo}/issues">${srepo}/issues</a> for problems with the site software</li>
    </ul>
</div>
