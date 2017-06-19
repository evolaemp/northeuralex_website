<%inherit file="app.mako"/>

<%block name="brand">
	<a href="${request.resource_url(request.dataset)}" class="brand">NorthEuraLex 0.9</a>
</%block>

<%block name="footer">
	<div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
		<div class="span4">
			<a href="http://www.sfs.uni-tuebingen.de/" title="Seminar für Sprachwissenschaft at the University of Tübingen">
				<img src="http://www.sfs.uni-tuebingen.de/~jvanrij/images/Uni.png" />
			</a>
		</div>
		<div class="span4" style="text-align: center;">
			<% license_icon = h.format_license_icon_url(request) %>
			% if license_icon:
			<a rel="license" href="${request.dataset.license}">
				<img alt="License" style="border-width:0" src="${license_icon}" />
			</a>
			<br />
			% endif
			${request.dataset.formatted_name()}
			is edited by
			<span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName" rel="cc:attributionURL">
				Johannes Dellert and Gerhard Jäger
			</span>
			and is licensed under the
			<a rel="license" href="${request.dataset.license}">${request.dataset.jsondata.get('license_name', request.dataset.license)}</a>.
			This research has been supported by the ERC Advanced Grant 324246 EVOLAEMP, which is gratefully acknowledged.
		</div>
		<div class="span4">
			<a href="http://www.evolaemp.uni-tuebingen.de/" title="Project EVOLAEMP">
				<img src="http://www.evolaemp.uni-tuebingen.de/img/logo.png" />
			</a>
		</div>
	</div>
</%block>

${next.body()}
