let img_inp = document.querySelector('input[type="file"]');
let img = document.querySelector('#image');
img_inp.onchange = function() {
  const [file] = img_inp.files
  if (file) {
    img.src = URL.createObjectURL(file)
  }
}

function loadURLToInputFiled(url, fileName){
  getImgURL(url, (imgBlob)=>{
    // Load img blob to input
    // WIP: UTF8 character error
    let file = new File([imgBlob], fileName,{type:"image/jpeg", lastModified:new Date().getTime()}, 'utf-8');
    let container = new DataTransfer();
    container.items.add(file);
    document.querySelector('input[type="file"]').files = container.files;

  })
}
// xmlHTTP return blob respond
function getImgURL(url, callback){
  var xhr = new XMLHttpRequest();
  xhr.onload = function() {
      callback(xhr.response);
  };
  xhr.open('GET', url);
  xhr.responseType = 'blob';
  xhr.send();
}