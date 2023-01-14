all:
	python3 set_root_password.py
	ansible-playbook webinar.yml -e 'webinar_set_psw=True'

