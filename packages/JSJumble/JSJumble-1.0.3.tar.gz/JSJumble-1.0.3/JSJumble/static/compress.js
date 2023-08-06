var isRequest = false
var successRequest
var failRequest
var isRequestInterval

var options

function requestFile(rel_dir,dir,sha){
    $.ajax({
        "url": "/get_file",
        "type": "POST",
        "Content-Type": "text/plain",
        "data": {
            "dir": dir,
        },
        success: function (data) {
            $("#console").append(`<span><span class="compressing">Compressing => </span>${dir}<span>`)
            let obfuscationResult = JavaScriptObfuscator.obfuscate(
                data,options
            )
            let content = obfuscationResult.getObfuscatedCode()
            $.ajax({
                "url": "/save_compressed",
                "type": "POST",
                "Content-Type": "application/javascript",
                "data": {
                    "rel_dir": rel_dir,
                    "dir": dir,
                    "sha": sha,
                    "content": content,
                },
                success: function (data) {
                    $("#console").append("<span class='success'>Successfully Compressed!</span>")
                    $("#console").append(`<span> <span>`)
                    successRequest += 1
                    isRequest = false
                },
                error: function (xhr, exception) {
                    $("#console").append("<span class='error'>[Error] Unable to Compress!</span>")
                    $("#console").append(`<span> <span>`)
                    failRequest += 1
                    isRequest = false
                }
            })
        },
        error: function (xhr, exception) {
            $("#console").append("<span class='error'>[Error] Unable to Compress!</span>")
            $("#console").append(`<span> <span>`)
            failRequest += 1
            isRequest = false
        }
    })
}

function requestDelete(){
    $("#console").append(`<span class='compressing'>Javascript is up to date, ${successRequest} changes applied! ${failRequest} failed!</span>`)
    $("#console").append(`<span> <span>`)
    $("#console").append(`<span class='starting'>[Checking & Removing] directory inside cache...</span>`)
    let element = document.getElementById("console");
    element.scrollTop = element.scrollHeight;
    $.ajax({
        "url": "/delete_unlist",
        "type": "POST",
        "Content-Type": "application/json",
        success: function (data) {
            if (data["result"] === "ignored_compress") $("#console").append(`<span class='compressing'>Completed!</span>`)
            else $("#console").append(`<span class='compressing'>Completed! ${data["result"]} directory removed inside compress folder.</span>`)
            
            let element = document.getElementById("console");
            element.scrollTop = element.scrollHeight;
            $("#start").prop('disabled', false);
        },
        error: function (xhr, exception) {
            $("#console").append("<span class='error'>[Error] Unable to do [Checking & Removing] directory inside cache!</span>")
            $("#console").append(`<span> <span>`)
            let element = document.getElementById("console");
            element.scrollTop = element.scrollHeight;
            $("#start").prop('disabled', false);
        }
    })
}

$(document).ready(function () {
    $("#start").on("click",function(){
        $("#start").prop('disabled', true);
        $("#console").html("<span class='starting'>Extracting Changed Static files...</span>")
        $("#console").append("<span class='starting'>Gathering Changed Javascript files...</span>")
        $("#console").append(`<span> <span>`)
        successRequest = 0
        failRequest = 0
        $.ajax({
            "url": "/get_change",
            "type": "GET",
            "Content-Type": "application/json",
            success: function (data) {
                options = data["engine"]
                data = data["data"]
                let i = 0
                isRequestInterval = setInterval(()=>{
                    if (data.length == 0){
                        clearInterval(isRequestInterval)
                        requestDelete()
                    }else{
                        if(i <= (data.length - 1)){
                            if (!isRequest){
                                isRequest = true
                                let rel_dir = data[i]["rel_dir"]
                                let base_path = data[i]["base_path"]
                                let sha512 = data[i]["sha"]
                                requestFile(rel_dir, base_path, sha512);
                                i += 1
                                let element = document.getElementById("console");
                                element.scrollTop = element.scrollHeight;
                            }
                        }else{
                            if (isRequest) return
                            clearInterval(isRequestInterval)
                            requestDelete()
                        }
                    }
                    
                })
            },
            error: function (xhr, exception) {
                $("#console").append("<span class='error'>[Error] Unable to start engine!</span>")
                $("#console").append(`<span> <span>`)
                let element = document.getElementById("console");
                element.scrollTop = element.scrollHeight;
                $("#start").prop('disabled', false);
            }
        })
    })
    
})