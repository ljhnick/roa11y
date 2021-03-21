var xmlhttp = new XMLHttpRequest();
xmlhttp.timeout = 1e9;

// ip_add = '131.179.6.13';
ip_add = 'localhost'
ip_port = 'http://' + ip_add + ':8090';

xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        console.log('server response: ' + xmlhttp.responseText);
    }
}