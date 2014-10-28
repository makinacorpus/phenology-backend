{% set cfg = opts.ms_project %}
{% set data = cfg.data %}
{% set scfg = salt['mc_utils.json_dump'](cfg) %}


echo {{cfg.name}}:
  cmd.run: 
    - name: |
            if [ -f {{data.py_root}}/bin/activate ];then . {{data.py_root}}/bin/activate;fi
            python manage.py build_tiles
    - user: {{cfg.user}}
    - cwd: {{data.app_root}}
    - env:
      - DJANGO_SETTINGS_MODULE: "{{data.DJANGO_SETTINGS_MODULE}}"
    
