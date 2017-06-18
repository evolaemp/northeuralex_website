<%inherit file="home_comp.mako"/>

<h3>Imprint</h3>

<p>
    Below is the information required by law about the web site of
    ${request.dataset.name}
    (${request.host_url}), an electronic resource published by
    ${request.dataset.publisher_name}
    as well as important legal points.
</p>

<h4>Data Protection</h4>
<h5>Data Collection and Processing</h5>
<p>
    Visits to this website are logged. The anonymized IP address currently used by your
    computer, as well as further technical data pertaining to the data call is recorded.
</p>
<p>
    Data is evaluated only for statistical purposes in anonymized form. No personal user
    profiles are created.
</p>
<p>
    Session cookies are used within the scope of this Internet session for technical
    reasons. This data is deleted at the latest when you close your browser.
</p>
<h5>Data Transmission</h5>
<p>
    Your personal data will only be transmitted to government organizations and
    authorities in legally required cases and/or for prosecution in the event of
    attacks on our network infrastructure. Your personal data are not provided to
    third parties for any other purpose.
</p>
<h4>Links to Websites of Third Parties</h4>
<p>
    This Website includes links to other external websites. These external links are
    designated with an icon as follows:
    ${h.external_link('http://example.org', 'external link')}.
    References to the subordinate pages of this Website are designated without an icon as
    follows: <a href="#">internal link example</a>.
</p>
