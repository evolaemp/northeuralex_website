<%inherit file="app.mako"/>

##
## define app-level blocks:
##
## <%block name="header">
##     <a href="${request.route_url('dataset')}">
##         <img src="${request.static_url('northeuralex:static/header.gif')}"/>
##     </a>
## </%block>

<%block name="brand">
	<a href="${request.resource_url(request.dataset)}" class="brand">NorthEuraLex</a>
</%block>

${next.body()}
