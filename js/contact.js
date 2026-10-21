(function(){
  var f=document.getElementById('f'),recap=document.getElementById('recap'),txt=document.getElementById('recap-txt'),ok=document.getElementById('ok');
  function v(id){return document.getElementById(id).value.trim()}
  function err(id,msg){document.getElementById('e-'+id).textContent=msg;var i=document.getElementById(id);i.setAttribute('aria-invalid',msg?'true':'false');return !msg}
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var tel=v('tel').replace(/[\s.\-]/g,'');
    var r=[
      err('nom',v('nom').length<2?'Indiquez votre nom.':''),
      err('tel',!/^(0|\+33|0033)[1-9]\d{8}$/.test(tel)?'Indiquez un numéro valide, par exemple 06 12 34 56 78.':''),
      err('type',!v('type')?'Choisissez un besoin.':''),
      err('msg',v('msg').length<10?'Décrivez votre projet en quelques mots (10 caractères minimum).':'')
    ];
    if(r.indexOf(false)>-1){f.querySelector('[aria-invalid="true"]').focus();recap.hidden=true;return}
    var t='Bonjour, je suis '+v('nom')+' ('+v('tel')+').\nBesoin : '+v('type')+'.\nProjet : '+v('msg')+'\nMerci de me recontacter.';
    txt.textContent=t;
    document.getElementById('sms').href='sms:+33635270651?&body='+encodeURIComponent(t);
    ok.textContent='';recap.hidden=false;recap.focus();
  });
  document.getElementById('copier').addEventListener('click',function(){
    var t=txt.textContent;
    function done(m){ok.textContent=m}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){done('Message copié.')},function(){fallback()})}else fallback();
    function fallback(){var r=document.createRange();r.selectNodeContents(txt);var s=getSelection();s.removeAllRanges();s.addRange(r);try{document.execCommand('copy');done('Message copié.')}catch(x){done('Sélectionnez le texte et copiez-le.')}}
  });
})();
