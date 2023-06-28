var velocidade = 50;
document.addEventListener('DOMContentLoaded', function() {
  atualizacaoPeriodicaPOS();
});

function atualizacaoPeriodicaPOS() {
  atualizarNumerosPos();

  intervalo = setInterval(function() {
    atualizarDados();
  }, 10000);
}

function atualizarNumerosPos() {
  var finalizados = 0;
  for(var i = 0; i < coresPOS.length; i++){
    document.getElementById(elementosPOS[i]).style.color = coresPOS[i];
  }


  var intervalo = setInterval(function() {
    finalizados = 0;

    for (var i = 0; i < elementosPOS.length; i++) {
      var elemento = document.getElementById(elementosPOS[i]);
      var valorAtual = Number(elemento.innerHTML);


      if (valorAtual < Number(numerosPOS[i])) {
        setValue(elemento, valorAtual + 1);
      } else if(valorAtual > Number(numerosPOS[i])){
        setValue(elemento, valorAtual - 1);
      } else{
        finalizados++;
      }
    }

    if (finalizados === elementosPOS.length) {
      clearInterval(intervalo); // Parar a execução quando todos os elementos estiverem atualizados
    }else{
      finalizados = 0;
    }
  }, velocidade);
}


function setValue(elemento, valor){
    if(valor < 10){ 
        elemento.innerHTML = String('0' + valor);
    } else {
        elemento.innerHTML = valor;
    }
}


// Função para atualizar os dados
function atualizarDados() {
  $.ajax({
      url: "/atualizar_dados",
      type: "GET",
      success: function(response) {
      // Atualize os elementos da página com os dados retornados
      numerosPOS[0] = response['em_aberto'][0];
      numerosPOS[1] = response['em_aberto'][1];
      numerosPOS[2] = response['em_aberto'][2];
      numerosPOS[3] = response['em_aberto'][3];
      numerosPOS[4] = response['finalizados'][0];
      numerosPOS[5] = response['sem_acesso'][0];
      numerosPOS[6] = response['sem_acesso'][1];
      coresPOS[1] = response['em_aberto'][4][1];
      coresPOS[2] = response['em_aberto'][4][2];
      coresPOS[3] = response['em_aberto'][4][0];
    }
  });
  atualizarNumerosPos();
}

