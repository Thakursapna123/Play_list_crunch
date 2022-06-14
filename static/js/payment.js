function getParameterByName(name){
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
    
    if (document.addEventListener){
    window.fpLayer = window.fpLayer || [];
    function fp() { fpLayer.push(arguments); }
    fp('config', 'client','<?php echo $qpayRadarID ?>' );
    fp('config', 'loaded', function (fp) {
    fp.send().then(function (data) {
    console.log(data.visitorId);
    if(!getParameterByName('fingerId')){
    window. location.href = window.location.href + "?fingerId=" + data.visitorId;
    }
    })
    });
    }