# ops-tools
Operation and maintenance personnel self-help gadget
## env
	E:\yc_study\github\ops-tools>python --version
	Python 3.6.3
	
	E:\yc_study\github\ops-tools>pip --version
	pip 9.0.2 from c:\python36\lib\site-packages (python 3.6)
## use
```Bash
git clone git@github.com:HanChengITer/ops-tools.git
cd ops-tools/
python -m venv ot_env
source ot_env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8080
```