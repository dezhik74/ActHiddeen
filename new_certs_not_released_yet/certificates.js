function makePicker(card, certList) {
  card.find('.cert-picker-row').empty()
  card.find('.cert-picker-row').append('<span>&nbsp;</span>')
  certList.filter((el) => el.checked).forEach((el)=> {
    card.find('.cert-picker-row').append(`
      <span class="badge badge-pill badge-secondary mb-1 mt-1 mr-1">${el.text}</span>
      `)
  })

}

// function removeAllModalListeners() {
//   $('#modalOkButton').off('click', okModal)
// }

$("#myModal").on('hidden.bs.modal', function (e) {
  okModal()
})

function okModal() {
  // получение списка отмеченных
  const certList = $("#modal").find(':checkbox').map(function () {
    return {
      value: this.value,
      text: $(this).siblings('label').html().trim(),
      checked: this.checked
    }
  }).get()

  // перенос списка отмеченных в пикер
  const current_card = $(`#${$('#modal').data().current_card}`)
  makePicker(current_card, certList)
  // перенос списка отмеченных в select
  $(`#${$('#modal').data().current_card}`).find('option').each(function (idx) {
    this.selected = certList[idx].checked
  })
  // removeAllModalListeners()
  $("#modal").modal('hide')
  
}
$('.cert-card').each( function() {
  $(this).on("click", (e) => {
    // заполнение модального окна
    const certList = $(e.target).closest(".cert-card").find('option').map( function () {
        return {
          value: this.value,
          text: this.text,
          selected: this.selected,
        }
      }
    ).get()
    $("#modal-body").html("")
    certList.forEach((cert) => {
      $("#modal-body").append(
        `
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${cert.value}" id="check-${cert.value}" ${cert.selected ? 'checked' : ''}>
            <label class="form-check-label" for="defaultCheck1">
              ${cert.text}
            </label>
          </div>
        `
      )
    })
    // сохраняем id карты, которую мы меняем
    $("#modal").data('current_card', $(e.target).closest(".cert-card").attr('id'))
    // навешивание кнопок 
    $('#modalOkButton').on('click', okModal)

    //открытие окна
    $('#modal').modal()
  })
})

$(document).ready(function() {
  $('.cert-card').each(function () {
    const certList = $(this).find('option').map(function () {
      return {
        value: this.value,
        text: this.text,
        checked: this.selected,
      }
    }).get()
    // console.log(certList)
    makePicker($(this), certList)
  })
})