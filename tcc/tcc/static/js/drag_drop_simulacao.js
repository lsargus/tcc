
var elementos;

function dragstart_handler(ev) {
 // Add the id of the drag source element to the drag data payload so
 // it is available when the drop event is fired
 ev.dataTransfer.setData("text/plain", ev.target.id);
 // Tell the browser both copy and move are possible
 ev.dataTransfer.effectAllowed = "copyMove";
 ev.dataTransfer.dropEffect = "copyMove";
}

function dragend_handler(ev) {
  // Remove all of the drag data
  ev.dataTransfer.clearData();
}

function dragover_handler(ev) {
 ev.preventDefault();
 ev.dataTransfer.dropEffect = "copyMove"
}

function drop_handler(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text/plain");
  var elemento_novo = document.getElementById(data).cloneNode(true);
  elemento_novo.id = uuidv4();

  var elemento_dados;

  ev.target.appendChild(elemento_novo);

  /*if (data === "barra_sist")
    elemento_dados = new Barra(elemento_novo.id);
  else if (data === "font_sist") {
    elemento_dados = new Equivalente(elemento_novo.id, '', '', '', '', '', '');
    }
  else if (data === "transf_sist") {
    elemento_dados = new Transformador(elemento_novo.id, '', '', '', '', '', '', '');
    }
  else if (data === "linha_sist") {
    var confirmButton = document.getElementById('confirLinha');
    var cancelButton = document.getElementById('cancel');
    $('#dialogLinha').modal('show');
	var targetDiv = ev.target;

    confirmButton.addEventListener('click', function() {
        var z1 = dlgLinha;

        elemento_dados = new Linha(elemento_novo.id, '', '', '', '', '');
		targetDiv.appendChild(elemento_novo);
        elementos = elementos.push(elemento_dados);
    });

    cancelButton.addEventListener('click', function() {
        favDialog.close();
    });
  }*/


}

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

class Elemento {
    constructor(id, z1, z0) {
        this.di = id;
    }

    conecta_elemento(link_d, link_e) {
        if (link_d != null)
            this.link_d = link_d;
        else
            this.link_e = link_e;
    }

    tem_conexao() {
        return !(this.link_d == null && this.link_e == null);
    }
}

class Equivalente extends Elemento {
    constructor(id, tensao_m, tensao_a, z1, z0, y1, y0) {
        super(id);
        this.z1 = z1;
        this.z0 = z0;
        this.tensao_m = tensao_m;
        this.tensao_a = tensao_a;
        this.y1 = y1;
        this.y0 = y0;
  }
}

class Linha extends Elemento {
    constructor(id, z1, z0, y1, y0, comp) {
        super(id);
        this.z1 = z1;
        this.z0 = z0;
        this.y1 = y1;
        this.y0 = y0;
        this.comp = comp;
  }
}

class Transformador extends Elemento {
    constructor(id, z1, z0, tensao_p, tensao_s, z_g1, z_g2, tipo) {
        super(id);
        this.z1 = z1;
        this.z0 = z0;
        this.tensao_p = tensao_p;
        this.tensao_s = tensao_s;
        this.z_g1 = z_g1;
        this.z_g2 = z_g2;
        this.tipo = tipo;
  }
}

class Barra extends Elemento {
    constructor(id) {
        super(id);
  }
}