window.onload = function () {
  // определяем функцию для кнопки добавить вверх
  let allUpButtons = document.querySelectorAll ('.up-add');
  Array.from(allUpButtons).map (function (item) {
    item.addEventListener('click', AddHAUp);
  })

  //определяем фунцию для кнопки добавить вниз
  let allDownButtons = document.querySelectorAll ('.down-add');
  Array.from(allDownButtons).map (function (item) {
    item.addEventListener('click', AddHADown);
  })

  //определяем функции для кнопки удалить карточку
  let allDelButtons = document.querySelectorAll ('.delete_ha');
  Array.from(allDelButtons).map (function (item) {
    item.addEventListener('click', DeleteHA);
  })

  //определяем функции для кнопки поменять содержимое с НИЖНЕЙ карточкой
  let allXChangeButtons = document.querySelectorAll ('.swap_ha');
  Array.from(allXChangeButtons).map (function (item) {
    item.addEventListener('click', SwapHA);
  })

}

function AddHAUp (event) {
  let haTotalForms = document.getElementById('id_hidden_acts-TOTAL_FORMS');
  // console.log ('Событие' + event.target.id);
  let haCard = this.parentNode.parentNode.parentNode;
  // console.log(haCard);
  let newHACard = haCard.cloneNode(true);
  haCard.before(newHACard);
  let newHACardItems = newHACard.querySelectorAll ('*');
  Array.from(newHACardItems).map (function (cardItem) {
    // console.log(cardItem.name + ' + ' + cardItem.value)
    if (cardItem.value != '') {
      cardItem.value = '';
      console.log(cardItem.name + ' + ' + cardItem.value)
    }
  })
  newHACard.querySelector('.down-add').addEventListener('click', AddHADown);
  newHACard.querySelector('.up-add').addEventListener('click', AddHAUp);
  newHACard.querySelector('.swap_ha').addEventListener('click', SwapHA);
  newHACard.querySelector('.delete_ha').addEventListener('click', DeleteHA);
  haTotalForms.value= Number (haTotalForms.value) + 1;
  RenumHACardsItems ();
}

function AddHADown (event) {
  let haTotalForms = document.getElementById('id_hidden_acts-TOTAL_FORMS');
  // console.log ('Событие' + event.target.id);
  let haCard = this.parentNode.parentNode.parentNode;
  // console.log(haCard);
  let newHACard = haCard.cloneNode(true);
  haCard.after(newHACard);
  let newHACardItems = newHACard.querySelectorAll ('*');
  Array.from(newHACardItems).map (function (cardItem) {
    if (cardItem.value != '') {
      cardItem.value = '';
    }
  })
  newHACard.querySelector('.down-add').addEventListener('click', AddHADown);
  newHACard.querySelector('.up-add').addEventListener('click', AddHAUp);
  newHACard.querySelector('.swap_ha').addEventListener('click', SwapHA);
  newHACard.querySelector('.delete_ha').addEventListener('click', DeleteHA);
  haTotalForms.value= Number (haTotalForms.value) + 1;
  RenumHACardsItems ();
}

function RenumHACardsItems () {
  let haCards = document.querySelectorAll('.ha-card');
  Array.from(haCards).map (function (oneHaCard, i) {
    let oneHaCardItems = oneHaCard.querySelectorAll('*');
    Array.from(oneHaCardItems).map(function (item) {
      if (item.id != '') {
        item.id = item.id.replace(/^id_hidden_acts-[0-9]+/, 'id_hidden_acts-' + i);
      }
      if (item.id != '') {
        item.name = item.name.replace(/^hidden_acts-[0-9]+/, 'hidden_acts-' + i);
      }
    })
  })
}

function DeleteHA () {
  let haTotalForms = document.getElementById('id_hidden_acts-TOTAL_FORMS');
  if (Number (haTotalForms.value) > 1) {
    if (confirm ('Точно удалить?')) {
      this.parentNode.parentNode.parentNode.remove();
      RenumHACardsItems ();
      haTotalForms.value= Number (haTotalForms.value) - 1;
    }
  } else {
      alert ('Нельзя удалить единственный акт!');
  }
}

function SwapHA () {
  let haCard = this.parentNode.parentNode.parentNode;
  //следующий сосед должен быть с классом .ha-card
  let nextHaCard = haCard.nextElementSibling;
  if (/ha-card/.test(nextHaCard.className)) {
    // берем номер id этой карты и следующего соседа
    let haCardId = this.id.match(/[0-9]+/)[0];
    let nextHaCardId = nextHaCard.firstElementChild.firstElementChild.nextElementSibling.firstElementChild.id.match(/[0-9]+/)[0];
    // console.log(haCard.querySelector('#id_hidden_acts-'+haCardId+'-act_number').value);
    //меняем номера акта
    Swap('-act_number');
    //меняем дату акта
    Swap('-act_date');
    //и так далее
    Swap('-begin_date');
    Swap('-end_date');
    Swap('-materials');
    Swap('-work_SNIP');
    Swap('-presented_work');
    Swap('-permitted_work');
    Swap('-docs');
    Swap('-annex');

    function Swap (part_of_id) {
      let swapper = haCard.querySelector('#id_hidden_acts-'+haCardId+part_of_id).value;
      haCard.querySelector('#id_hidden_acts-'+haCardId+part_of_id).value = nextHaCard.querySelector('#id_hidden_acts-'+nextHaCardId+part_of_id).value;
      nextHaCard.querySelector('#id_hidden_acts-'+nextHaCardId+part_of_id).value = swapper;
    }
  }
}