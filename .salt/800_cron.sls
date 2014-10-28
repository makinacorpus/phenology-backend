{% set cfg = opts.ms_project %}
{% set data = cfg.data %}
{% set scfg = salt['mc_utils.json_dump'](cfg) %}

{{cfg.name}}-cron:
  file.managed:
    - name: {{cfg.data_root}}/{{cfg.name}}-cron
    - mode: 700
    - user: root
    - source: ''
    - contents: |
                #!/usr/bin/env bash
                LOG="{{cfg.data_root}}/{{cfg.name}}.log"
                lock="${0}.lock"
                if [ -e "${lock}" ];then
                  echo "Locked ${0}";exit 1
                fi
                touch "${lock}"
                salt-call --local --out-file="${LOG}" --retcode-passthrough -lall --local mc_project.run_task {{cfg.name}} task_cron 1>/dev/null 2>/dev/null
                ret="${?}"
                rm -f "${lock}"
                if [ "x${ret}" != "x0" ];then
                  cat -e "${LOG}"
                fi
                exit "${ret}"

{{cfg.name}}-cron-crond:
  file.managed:
    - watch:
      - file: {{cfg.name}}-cron
    - name: /etc/cron.d/{{cfg.name}}-cron
    - mode: 700
    - user: root
    - source: ''
    - contents: |
                #!/usr/bin/env bash
                MAILTO="{{cfg.data.adminmail}}"
                {{data.periodicity}} root {{cfg.data_root}}/{{cfg.name}}-cron
