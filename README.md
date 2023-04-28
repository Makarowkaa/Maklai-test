# django_syntax_tree
### Test task for Maklai.

### How to install using GitHub
```
git clone https://github.com/Makarowkaa/django_syntax_tree.git
cd django_syntax_tree
python -m venv venv
source venv/Scripts/activate # for Windows using Bash
or
source venv/bin/activate # for Linux
pip install -r requirements.txt
```
### How to run and use:
```
python manage.py runserver
```

Use this URL in your browser:
```
http://localhost:8000/paraphrase?tree=input_tree&limit=input_limit
```

Change input_tree and input_limit for the desired ones

URL to use as it defined in the task:
```
localhost:8000/paraphrase?tree=(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )
```