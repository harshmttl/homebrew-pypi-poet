from textwrap import dedent

from jinja2 import Environment

from .util import dash_to_studly


env = Environment(trim_blocks=True)
env.filters["dash_to_studly"] = dash_to_studly


FORMULA_TEMPLATE = env.from_string(dedent("""\
    class {{ package.name|dash_to_studly }} < Formula
      include Language::Python::Virtualenv
        url "{{ package.url }}"{% if package.vcs %}, :using => :{{package.vcs}}{% endif %}{% if package.branch %}, :branch => "{{ package.branch }}"{% endif %}
        {% if package.checksum %}sha256 "{{ package.checksum }}"{% endif %}

      {% if package.version %}version "{{package.version}}"{% endif %}


      depends_on {% raw %}"python@3.9"{% endraw %}

    {% if resources %}
    {%   for resource in resources %}

    {%     include ResourceTemplate %}

    {%   endfor %}
    {% endif %}


      def install
        virtualenv_install_with_resources
      end

      test do
        false
      end
    end
    """))


RESOURCE_TEMPLATE = env.from_string("""\
  resource "{{ resource.name }}" do
    url "{{ resource.url }}"{% if resource.vcs %}, :using => :{{resource.vcs}}{% endif %}{% if resource.branch %}, :branch => "{{ resource.branch }}"{% endif %}{% if resource.revision %}, :revision => "{{ resource.revision}}"{% endif %}
{%if resource.checksum %}

    {{resource.checksum_type}} "{{ resource.checksum }}"
{% else %}

{% endif %}
  end
""")
