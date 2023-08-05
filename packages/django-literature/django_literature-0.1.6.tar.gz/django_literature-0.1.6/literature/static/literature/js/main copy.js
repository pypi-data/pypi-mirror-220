const Cite = require('citation-js')

var data;

function updatePreview(data) {
  document.getElementById("preview").innerHTML = data.format('bibliography', {
    format: 'html',
    template: 'apa',
    lang: "{{ lang_code }}"
  })
}

async function readFileContents(e) {
  const file = e.target.files.item(0)
  const content = await file.text();
  data = await Cite.Cite(content)
  updatePreview(data)
}

async function getData(lookup) {
  data = await Cite.Cite(lookup)
  updatePreview(data)
};

function fetchReference() {
  getData(document.getElementById('inputDOI').value)
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function submit() {

  $.ajax({
    url: '/submit-csl/',
    type: 'post',
    dataType: 'json',
    success: function (data) {
        $('#response').html(data.msg);
    },
    data: {data: JSON.stringify(data.format('data',{format:'object'}))}
  });
};