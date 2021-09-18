from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'nome_pag': 'Sobre'})


def projeto(request):
    return render(request, 'projeto.html',
                  {'nome_pag': 'Projeto',
                   'links': [['stylesheet',
                              'text/css',
                              'css/drag_drop_simulacao.css'], ],
                   'scripts': [['text/javascript',
                                'js/drag_drop_simulacao.js'], ]})
