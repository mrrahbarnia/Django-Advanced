{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password
{% endblock %}


{% block html %}
<h1>Hello {{user}}</h1>
<hr>
<a href={{link}}>Click here</a>
{% endblock %}