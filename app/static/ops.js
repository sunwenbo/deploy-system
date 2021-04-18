
//这个是全局的定时器。
var timeout ;
var timeout1 ;
var timeout2 ;


$("body").on('click', '#del_project', function(){
    var project = $('#ipt_project').val()
    if (confirm('请确认删除项目及关联主机信息: '+project)) {
        var param = {
            project: project
        }
        $.post('/del_project', param, function(data){
            alert("删除项目 "+project+"  status: "+data.status+" log: "+data.log);
            if (data.status == 'ok') {
                project_list();
                $('#project_div').html("");
                $('#add_host_table').html("");
                $('#hostManage').html("");
                $('#host').html("");
            }
        }, 'json');
    };
});


function push_add_host_table(p){
    var project = p
    var param = {
        project: project
    }
    //$.getJSON('/project_info', param, function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>ip(*必填)</th><th>主机类型</th><th>pnum(进程数)</th><th>env(进程环境变量)</th><th>addhost</th></thead>');
        htm.push('<tr>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_ip" placeholder="10.10.10.10" value="">'+'</td>');
        htm.push('<td>'+'<select class="form-control" id="add_hosttype"><option value="FlowNormal" selected = "selected">FlowNormal</option><option value="FlowSmall">FlowSmall</option><option value="Batch">Batch</option><option value="Crontab">Crontab</option><option value="Fix">Fix</option></select>'+'</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_pnum" style="width:60px;" placeholder="" value="1">'+'</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_env" placeholder="a=1,b=/data/" value="">'+'</td>');
        htm.push('<td><button id="add_host" class="btn btn-small btn-success" project="'+project+'" >添加主机</button></td>');
        htm.push('</tr>');
        htm.push('</table>');
        $('#add_host_table').html(htm.join(''));
    //})
};


$("body").on('click', '#add_newproject', function(){
    if (confirm('请确认项目信息')) {
        var add_group = $('#add_group').val()
        var add_environment = $('#add_environment').val()
        var add_k8sclustername = $('#add_k8sclustername').val()
        var add_namespace = $('#add_namespace').val()
        var add_p = $('#add_p').val()
        var add_codetype = $('#add_codetype').val()
        var add_port = $('#add_port').val()
        var add_git = $('#add_git').val()
        var add_branch = $('#add_branch').val()
        var add_config = $('#add_config').val()
        //var add_make = $('#add_make').val()
        var add_start = $('#add_start').val()
        var add_remarks = $('#add_remarks').val()
        var add_makepath = $('#add_makepath').val()

        if(!add_group ){
            alert('group null');
            return false;
        }

        if(!add_environment ){
            alert('environment null');
            return false;
        }
        if(!add_p ){
            alert('project null');
            return false;
        }
        if(!add_codetype){
            alert('type null');
            return false;
        }
        if(parseInt(add_port)>65535){
            alert('error: port > 65535');
            return false;
        }

        var param = {
            group: add_group,
            environment: add_environment,
            k8sclustername: add_k8sclustername,
            namespace: add_namespace,
            p: add_p,
            codetype: add_codetype,
            port: add_port,
            git: add_git,
            branch: add_branch,
            config: add_config,
            //make: add_make,
            start: add_start,
            remarks: add_remarks,
            makepath: add_makepath
        }

        $.post('/add_project', param, function(data){
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});



$("body").on('click', '#update_project', function(){
    if (confirm('请确认项目信息')) {
        var add_project       = $('#add_project').val()
        var add_group         = $('#add_group').val()
        var add_environment   = $('#add_environment').val()
        var add_p             = $('#add_p').val()
        var add_codetype      = $('#add_codetype').val()
        var add_port          = $('#add_port').val()
        var add_git           = $('#add_git').val()
        var add_branch        = $('#add_branch').val()
        var add_config        = $('#add_config').val()
        var add_make          = $('#add_make').val()
        var add_start         = $('#add_start').val()
        var add_remarks       = $('#add_remarks').val()
        var add_dockerfile    = $('#add_dockerfile').val()
        var add_k8syaml       = $('#add_k8syaml').val()
        var add_makepath      = $('#add_makepath').val()
        var add_k8smanagename = $('#add_k8smanagename').val()
        var add_nodeport      = $('#add_nodeport').val()
        var add_namespace     = $('#add_namespace').val()

        if(!add_environment){
            alert('environment null');
            return false;
        }
        if(!add_branch){
            alert('git branch null');
            return false;
        }
        if(!add_project){
            alert('project null');
            return false;
        }
        if(!add_codetype){
            alert('codetype null');
            return false;
        }
        if(parseInt(add_port)>65535){
            alert('error: port > 65535');
            return false;
        }
        var param = {
            project      : add_project,
            group        : add_group,
            environment  : add_environment,
            p            : add_p,
            codetype     : add_codetype,
            port         : add_port,
            git          : add_git,
            branch       : add_branch,
            config       : add_config,
            make         : add_make,
            start        : add_start,
            remarks      : add_remarks,
            dockerfile   : add_dockerfile,
            k8syaml      : add_k8syaml,
            makepath     : add_makepath,
            k8smanagename: add_k8smanagename,
            nodeport     : add_nodeport,
            namespace    : add_namespace
        }

        $.post('/update_project', param, function(data){
            alert(data.status+"  "+data.log);
            //if(data.status == 'ok'){
            //    $('#project_div').html("");
            //    $('#project_div').attr('status','close')
            //    project_list();
            //}
        }, 'json');
    };
});



function push_add_project_table(){

    $.getJSON('/group_list', function(groupdata){
    $.getJSON('/codetype_list_all', function(codetypedata){
    $.getJSON('/environment_list_all', function(environmentdata){

    var htm=['<table class="table table-hover ">'];

    htm.push('<tr>');
    htm.push('<td width="120" align="right">group:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_group">');
    for(var i=0,len=groupdata.length; i<len; i++){
        htm.push('<option value="'+groupdata[i]+'">'+groupdata[i]+'</option>');
    }
    htm.push('</select></td>');
    htm.push('<td>选择分组(管理员权限-项目管理页面添加,人员也要添加对应分组权限)</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">environment:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_environment" onchange="get_k8sclustername()">');
    for(var i=0,len=environmentdata.length; i<len; i++){
        htm.push('<option value="'+environmentdata[i]+'">'+environmentdata[i]+'</option>');
    }
    htm.push('</select></td>');
    htm.push('<td>选择环境(管理员权限-项目管理页面添加)</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">k8scluster:</td>');
    htm.push('<td><div id="k8sclustername">');
    htm.push('</div></td>');
    htm.push('<td>选择k8s集群(管理员权限-项目管理页面添加)</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">k8s-namespace:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_namespace" placeholder="default" value="default">'+'</td>');
    htm.push('</div></td>');
    htm.push('<td>使用k8s集群的namespace</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">codeType:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_codetype">');
    for(var i=0,len=codetypedata.length; i<len; i++){
        htm.push('<option value="'+codetypedata[i]+'">'+codetypedata[i]+'</option>');
    }
    htm.push('</select></td>');
    htm.push('<td>选择代码类型(关联操作模板文件)(管理员权限-项目管理页面添加,并设置对应模板)</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">projectName:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_p" placeholder="post" value="">'+'</td>');
    htm.push('<td>填写服务名(a-z,-,0-9)不允许全数字,例子:pp-qwer-asd</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">git:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="git://github.com/sre/op.git" value="">'+'</td>');
    htm.push('<td>git仓库地址,重要:git协议的地址</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">branch:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_branch" placeholder="master" value="master">'+'</td>');
    htm.push('<td>git仓库的代码分支,默认:master</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">port:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_port" placeholder="go port[8000-10000]  nodejs port[3000-5000] python port [5000-7000]" value="">'+'</td>');
    htm.push('<td>docker内部进程启动的默认监听端口:8080</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">makepath:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_makepath" placeholder="./" value="./">'+'</td>');
    htm.push('<td>由于git仓库目录较多,指定代码的编译目录</td>');
    htm.push('</tr>');

    //htm.push('<tr>');
    //htm.push('<td width="120" align="right">make:</td>');
    //htm.push('<td>'+'<textarea id="add_make" rows="5" cols="100"  >'+''+'</textarea>'+'</td>');
    //htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">config(name=subPath):</td>');
    htm.push('<td>'+'<textarea id="add_config" rows="5" cols="100"  >'+''+'</textarea>'+'</td>');
    htm.push('<td>配置文件,会自动生成yaml中subPath对应的配置文件名</td>');
    htm.push('</tr>');
    //htm.push('<tr>');
    //htm.push('<td width="120" align="right">start:</td>');
    //htm.push('<td>'+'<textarea id="add_start" rows="5" cols="100"  >'+''+'</textarea>'+'</td>');
    //htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">remarks:</td>');
    htm.push('<td>'+'<textarea id="add_remarks" rows="5" cols="100"  >'+''+'</textarea>'+'</td>');
    htm.push('<td>备注</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td></td>');
    htm.push('<td><button id="add_newproject" class="btn btn-small btn-success" >添加新项目</button></td>');
    htm.push('</tr>');
    htm.push('<td></td>');
    htm.push('</table>');

    $('#project_div').html(htm.join(''));

    get_k8sclustername();
    })
    })
    });
};

function get_k8sclustername(){
    var environment = $('#add_environment').val()
    var param = {
        environment: environment
    }
    $.getJSON('/get_k8sclustername', param , function(data){
        var htm=['<select class="form-control" id="add_k8sclustername">'];
        for(var i=0,len=data.data.length; i<len; i++){
            htm.push('<option value="'+data.data[i]+'">'+data.data[i]+'</option>');
        }
        htm.push('</select>');
        $('#k8sclustername').html(htm.join(''));
    });
}

$("body").on('click', '#add_host', function(){
    if (confirm('确认提交？')) {
        var add_hostname = $('#add_hostname').val()
        var add_ip       = $('#add_ip').val()
        var add_project  = $('#add_host').attr('project')
        var add_hosttype = $('#add_hosttype').val()
        var add_pnum     = $('#add_pnum').val()
        var add_env      = $('#add_env').val()
        var param = {
            hostname: add_hostname,
            ip      : add_ip,
            project : add_project,
            hosttype: add_hosttype,
            pnum    : add_pnum,
            env     : add_env
        }

        $.post('/add_host', param, function(data){
            //host_list_table(add_project)
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#add_newgroup', function(){
    //界面判断是否确认
    if (confirm('确认提交？')) {
        //从project_admin.html页面获取addgroupname变量
        var addgroupname = $('#addgroupname').val()
        //新建一个param的字典将输入新建组的名称赋值
        var param = {
            addgroupname: addgroupname,
        }
        //调用views.py中add_group，将param作为参数传值
        $.post('/add_group', param, function(data){
            //调用ops.js中group_list_all函数
            group_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});

$("body").on('click', '#add_newenvironment', function(){
    if (confirm('确认提交？')) {
        var addenvironmentname = $('#addenvironmentname').val()
        var param = {
            addenvironmentname: addenvironmentname,
        }
        $.post('/add_environment', param, function(data){
            environment_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});

$("body").on('click', '#add_newcodetype', function(){
    if (confirm('确认提交？')) {
        var addcodetypename = $('#addcodetypename').val()
        var param = {
            addcodetypename: addcodetypename,
        }
        $.post('/add_codetype', param, function(data){
            codetype_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#del_group', function(){
    if (confirm('确认删除服务组？')) {
        var selectgroup = $('#selectgroup').val()
        var param = {
            selectgroup: selectgroup,
        }
        $.post('/del_group', param, function(data){
            group_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});

$("body").on('click', '#del_environment', function(){
    if (confirm('确认删除空环境？')) {
        var selectenvironment = $('#selectenvironment').val()
        var param = {
            selectenvironment: selectenvironment,
        }
        $.post('/del_environment', param, function(data){
            environment_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});

$("body").on('click', '#del_codetype', function(){
    if (confirm('确认删除无用的代码类型？')) {
        var selectcodetype = $('#selectcodetype').val()
        var param = {
            selectcodetype: selectcodetype,
        }
        $.post('/del_codetype', param, function(data){
            codetype_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#add_servergroup', function(){
    if (confirm('确认提交？')) {
        var username = $('#current_user').val()
        var servicegroup = $('#add_server_group').val()
        var permissions = $('#add_permissions').val()
        var param = {
            username: username,
            servicegroup: servicegroup,
            permissions: permissions,
        }
        $.post('/adduserservicegroup', param, function(data){
            alert(data.status+"  "+data.log);
            userservicegrouplist(username);
            servergroup_list_all()
        }, 'json');
    };
});



$("body").on('click', '#delete_servergroup', function(){
    if (confirm('确认提交？')) {
        var username = $(this).attr('username')
        var servicegroup = $(this).attr('servergroup')
        var param = {
            user: username,
            servicegroup: servicegroup,
        }
        $.post('/deleteuserservicegroup', param, function(data){
            alert(data.status+"  "+data.log);
            userservicegrouplist(username);
        }, 'json');
    };
});



$("body").on('click', '#delete_user', function(){
    if (confirm('确认提交？')) {
        var username = $(this).attr('username')
        var param = {
            deleteuser: username,
        }
        $.post('/delete_user', param, function(data){
            alert(data.status+"  "+data.log);
            user_list();
        }, 'json');
    };
});



$("body").on('click', '#add_user', function(){
    if (confirm('确认提交？')) {
        var username = $('#addusername').val()
        var password = $('#addpassword').val()
        var param = {
            adduser: username,
            password: password,
        }
        $.post('/add_user', param, function(data){
            alert(data.status+"  "+data.log);
            user_list();
        }, 'json');
    };
});



$("body").on('click', '#update_host', function(){
    var num      = $(this).attr('i')
    var project  = $(this).attr('project')
    var hostname = $('#hostname'+num).val()
    var hostip   = $('#hostip'+num).val()
    var hosttype = $('#hosttype'+num).val()
    var pnum     = $('#pnum'+num).val()
    var env      = $('#env'+num).val()

    if (confirm('请确认更新: '+host)) {
        var param = {
            project:   project,
            hostname:  hostname,
            hostip:    hostip,
            hosttype:  hosttype,
            pnum:      pnum,
            env:       env
        }
        $.post('/update_host', param, function(data){
            //host_list_table(project)
            alert(data.status+"  "+data.log);
        }, 'json');
    }
});


$("body").on('click', '#del_host', function(){
    var host = $(this).attr('host')
    var project = $(this).attr('project')
    if (confirm('请确认删除: '+host)) {
        var param = {
            host:    host,
            project: project,
        }
        $.post('/del_host', param, function(data){
            //host_list_table(project)
            //hostmanage_list_table(project)
            alert(data.status+"  "+data.log);
        }, 'json');
    }
});



$("#back_submit").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p == undefined){
        alert('project null');
        return false;
    }
    var fastback = $('#fastback').val()
    if (fastback == 'yes'){
        if (confirm('快速回滚: '+ p +'？ 仅限在有故障时紧急操作,不是平滑操作,服务接口会有大量报错,也不做任何检查.')) {
            var operation = 'serviceFastback'
        }else{
            return false;
        };
    }else{
        var operation = 'serviceFallback'
    }

    var param = {
        project: p,
        operation: operation,
        tag: $('#select_tag').val(),
    };

    $.getJSON('/lock_check', param, function(data){
        if(data['status'] == "ok"){
            if (confirm('请确认回滚'+ p +'？')) {
                updateonline(param)
            };
        }else{
            alert(data['user'] + '正在操作，请勿重复执行！')
        }
    });
});



$("body").on('click', '#btn_submit', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        var param = {
            operation: 'serviceUpdate',
            project: p,
        };
        $.getJSON('/lock_check', param, function(data){
            if(data['status'] == "ok"){
                if (confirm('请确认更新' + p + '并重启服务!\u000d重要: 请确认数据库索引已经提前创建')) {
                    updateonline(param)
                    online_tag(p)
                    current_tag(p)
                    get_svcadd(p)
                };
            }else{
                alert(data['user'] + '正在操作' + p + '，请勿重复执行！')
            }
        });
    }
    else{
        alert('project null');
    };
});


$("#restart_submit").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        var param = {
            operation: 'serviceRestart',
            project: p,
        };
        $.getJSON('/lock_check', param, function(data){
            if(data['status'] == "ok"){
                if (confirm('请确认重启'+ p +'服务!')) {
                    updateonline(param)
                };
            }else{
                alert(data['user'] + '正在操作，请勿重复执行！')
            }
        });
    }
    else{
        alert('project null');
    };
});



function updateonline(param){
    if (param['operation'] == 'serviceStop'){
        var num = 1;
    } else {
        var chks = $('.hostList input:checkbox:checked');
        var num = chks.length;
        //if(num==0){
        //    alert('host list null')
        //    return
        //}
        var _arr=[];
        for(var i=0,len=num; i<len; i++){
            _arr.push(chks[i].value) ;
        }
        param.client = _arr.join(",");
    }

    console.log(param);

    $.post('/deploy', param, function(data){
        $("#resDiv").html( "operation:&nbsp;"+data.operation+
            "<br>project:&nbsp;"+data.project+
            "<br>taskid:&nbsp;"+data.taskid+
            "<br>tag:&nbsp;"+data.tag+
            "<br>status:&nbsp;"+data.status+
            "<br>logout:&nbsp;"+data.output
            );
        if(data.status == 'wait'){
            $('#ProgressBarDiv').html("");
            if(timeout){clearInterval(timeout)};
            timeout = setInterval(function(){
                next(data.taskid, 3);
            },4000);
            $('#cnt').html("");
        } else {
            alert(data.status + '  ' + data.output)
        };
    }, 'json');
};


function pagelist(){
    $.getJSON('/pagelist',  function(data){
        var htm=['<ul class="nav nav-pills navbar-left" role="tablist">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<li role="presentation"><a class="presentationLink" href="/'+data[i][0]+'">'+data[i][1]+'</a></li>');
        }
        htm.push('</ul>');
        $('#pagelist').html(htm.join(''));
    });
};



function project_list(p){

    var selectgroup = $('#selectgroup').val()
    var functype = $('#leftDiv').attr('path')
    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'group', selectgroup)
        $v.attr('href', newHref)
    })
    var param = {
        group: selectgroup,
        functype: functype
    }

    $.getJSON('/project', param , function(data){

        var htm=[''];
        $.each(data, function(g, projectlist){
            htm.push('<a href="#'+g+'" class="nav-header menu-first collapsed" data-toggle="collapse" aria-expanded="false"><i class="icon-user-md icon-large"></i><h4>'+g+'</h4></a>');
            htm.push('<ul id="'+g+'" class="collapse in" >');

            var h=projectlist.sort();
            for(var i=0,len=h.length; i<len; i++){

                if(functype == "online"){
                    htm.push('<li ><a id="'+h[i]+'" class="host_list" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                if(functype == "project_admin"){
                    htm.push('<li ><a id="'+h[i]+'" class="host_list_admin" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                if(functype == "online_log"){
                    htm.push('<li ><a id="'+h[i]+'" class="online_log_time" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                htm.push('<p class="text-success">'+h[i]+'</p>');
                htm.push('</a></li>');
            }
            htm.push('</ul><br>');
        })
        $('#project').html(htm.join(''));
        $('#project_div').attr('status','close');

        if (p != undefined ) {
            if(functype == "online"){
                host_list_push(p);
            }
            if(functype == "project_admin"){
                console.log('project_admin');
                $('p').css('background','');
                $($('[data-project="'+p+'"]').find('p')[0]).css({"backgroundColor":"#C1FFC1"});
            }
        }
        jump()
    });
};

function jump(){
    var id = parseQuery().project
    if(id){
        var el = $('#' + id)[0]
        el.scrollIntoView({behavior: 'smooth'})
    }
};

function group_list(){

    var url=window.location.search.substr(1).split("&")
    var avgr = new Array();

    for (var i = 0; i < url.length; i++){
        avgr[url[i].split('=')[0]] = url[i].split('=')[1];
    }
    $.getJSON('/group_list', function(data){
        var htm=['<select class="form-control" id="selectgroup" onchange="project_list()">'];
        for(var i=0,len=data.length; i<len; i++){
            if (avgr['group'] == data[i]){
                htm.push('<option value="'+data[i]+'" selected="selected">'+data[i]+'</option>');
            } else{
                htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
            }
        }
        htm.push('</select>');
        $('#group').html(htm.join(''));
        project_list(avgr['project']);
    })
};

function group_list_all(){
    //调用views.py group_list_all函数将数据库的返回，显示在前端
    $.getJSON('/group_list_all', function(data){
        var htm=['<select class="form-control" id="selectgroup">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#groupnamediv').html(htm.join(''));
    })
};

function environment_list_all(){
    $.getJSON('/environment_list_all', function(data){
        var htm=['<select class="form-control" id="selectenvironment">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#environmentnamediv').html(htm.join(''));
    })
};

function codetype_list_all(){
    $.getJSON('/codetype_list_all', function(data){
        var htm=['<select class="form-control" id="selectcodetype">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#codetypenamediv').html(htm.join(''));
    })
};

function user_list(){
    $.getJSON('/user_list', function(data){
        var htm=['<ul type="disc">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<li><a class="userlist" username="'+data[i]+'">'+data[i]+'</a></li>');
        }
        htm.push('</ul>');
        $('#user_list').html(htm.join(''));
    })
};



$("body").on('click', '.userlist', function(){
    var username = $(this).attr('username')
    userservicegrouplist(username)
    servergroup_list_all()
});


function userservicegrouplist(username){
    var param = {
        user: username
    }

    $.getJSON('/userservicegrouplist', param, function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>username</th><th>server group</th><th>permissions</th><th>operation</th></thead>');
        htm.push('<tr>');
        htm.push('<td>'+'<input type="text" readonly="true" id="current_user" class="form-control"  value="'+username+'">'+'</td>');
        htm.push('<td>'+'<div id="usergroupnamediv" class="sidebar-menu"></div>'+'</td>');
        htm.push('<td>'+'<select class="form-control" id="add_permissions"><option value="developer">developer</option><option value="config">config</option><option value="online" selected="selected">online</option></select>'+'</td>');
        htm.push('<td>'+'<button id="add_servergroup" class="btn btn-small btn-success">添加组权限</button>'+'</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+username+'">'+'</td>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+data[i][0]+'">'+'</td>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+data[i][1]+'">'+'</td>');
            htm.push('<td>'+'<button id="delete_servergroup" username="'+username+'" servergroup="'+data[i][0]+'" class="btn btn-small btn-danger">删除组权限</button>'+'</td>');
            htm.push('</tr>');
        }

        htm.push('<tr>');
        htm.push('<td>'+'<button id="delete_user" username="'+username+'" class="btn btn-small btn-danger">删除用户</button>'+'</td>');
        htm.push('</tr>');

        htm.push('</table>');
        $('#update_user').html(htm.join(''));
    })
}


function servergroup_list_all(){
    $.getJSON('/group_list_all', function(data){
        var htm=['<select class="form-control" id="add_server_group">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#usergroupnamediv').html(htm.join(''));
    })
};


function host_list_table(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>hostname</th><th>ip</th><th>hosttype</th><th>pnum</th><th>status</th><th>UpTime</th><th>consul</th><th>CheckTime</th><th>commitID</th><th>Tag</th><th>stop</th></thead>');
        if (data.data!='' && data.data!=undefined && data.data!=null){
            for(var i=0,len=data.data.length; i<len; i++){
                htm.push('<tr>');
                if (p.indexOf("online")!=0){
                    htm.push('<td>'+'<input type="checkbox" name="onlinehost" value="'+data.data[i].ip+'" checked="checked">'+data.data[i].hostname+'</td>');
                } else {
                    htm.push('<td>'+'<input type="checkbox" name="onlinehost" value="'+data.data[i].ip+'" >'+data.data[i].hostname+'</td>');
                }
                htm.push('<td>'+data.data[i].ip+'</td>');
                htm.push('<td>'+data.data[i].hosttype+'</td>');
                htm.push('<td>'+data.data[i].pnum+'</td>');
                if(data.data[i].checkstatus == "RUNNING" || data.data[i].checkstatus == "Up" ){
                    htm.push('<td><div id="status'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu"><font color="Lime">'+data.data[i].checkstatus+'</font></div></td>');
                } else if(data.data[i].checkstatus == "SSHOK"){
                    htm.push('<td><div id="status'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu"><font color="#FF9900">'+data.data[i].checkstatus+'</font></div></td>');
                } else {
                    htm.push('<td><div id="status'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu"><font color="red">'+data.data[i].checkstatus+'</font></div></td>');
                }
                htm.push('<td><div id="UpTime'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu">'+data.data[i].checktime+'</div></td>');
                if(data.data[i].checkconsulstatus == "ok"){
                    htm.push('<td><div id="checkconsulstatus'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu"><font color="Lime">'+data.data[i].checkconsulstatus+'</font></div></td>');
                } else {
                    htm.push('<td><div id="checkconsulstatus'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu"><font color="red">'+data.data[i].checkconsulstatus+'</font></div></td>');
                }
                htm.push('<td><div id="checkconsultime'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu">'+data.data[i].checkconsultime+'</div></td>');
                htm.push('<td><div id="commitID'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu">'+data.data[i].commitid+'</div></td>');
                htm.push('<td><div id="Tag'+data.data[i].ip.replace(/\./g,"-")+'" class="sidebar-menu">'+data.data[i].updatetime+'</div></td>');
                htm.push('<td>'+'<a href="javascript:;" onclick=stop_submit("'+data.data[i].ip+'");>stop</a>'+'</td>');
                htm.push('</tr>');
            }
        }
        htm.push('</table>');
        $('#host').html(htm.join(''));
    });
};


function hostmanage_list_table(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>hostname</th><th>ip</th><th>hosttype</th><th>pnum</th><th>ENV</th><th>status</th><th>save</th><th>delete</th></tr></thead>');
        if (data.data!='' && data.data!=undefined && data.data!=null){
            for(var i=0,len=data.data.length; i<len; i++){
                htm.push('<tr>');
                htm.push('<td>'+'<input type="text" class="form-control" id="hostname'+i+'" placeholder="hostname" value="'+data.data[i].hostname+'">'+'</td>');
                htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="hostip'+i+'" placeholder="data.data[i].ip" value="'+data.data[i].ip+'">'+'</td>');
                htm.push('<td>'+'<input type="text" class="form-control" id="hosttype'+i+'" placeholder="hosttype" style="width:60px;" value="'+data.data[i].hosttype+'">'+'</td>');
                htm.push('<td>'+'<input type="text" class="form-control" id="pnum'+i+'" placeholder="pnum" style="width:60px;" value="'+data.data[i].pnum+'">'+'</td>');
                htm.push('<td>'+'<input type="text" class="form-control" id="env'+i+'" placeholder="a=1,b=2" value="'+data.data[i].env+'">'+'</td>');
                if(data.data[i].checkstatus == "RUNNING" || data.data[i].checkstatus == "Up"){
                    htm.push('<td>'+'<font color="Lime">'+data.data[i].checkstatus+'</font>'+'</td>');
                } else if(data.data[i].checkstatus == "SSHOK"){
                    htm.push('<td>'+'<font color="#FF9900">'+data.data[i].checkstatus+'</font>'+'</td>');
                }else{
                    htm.push('<td>'+'<font color="red">'+data.data[i].checkstatus+'</font>'+'</td>');
                }
                htm.push('<td><button id="update_host" host="'+data.data[i].ip+'" i="'+i+'" class="btn btn-sm btn-info" project="'+p+'" >保存</button></td>');
                htm.push('<td><button id="del_host" host="'+data.data[i].ip+'" class="btn btn-sm btn-danger" project="'+p+'" >删除主机</button></td>');
                htm.push('</tr>');
            }
        }
        htm.push('</table>');
        $('#hostManage').html(htm.join(''));
    });
};


function host_list_status(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        if (data.data!='' && data.data!=undefined && data.data!=null){
            for(var i=0,len=data.data.length; i<len; i++){
                if(data.data[i].checkstatus == "RUNNING" || data.data[i].checkstatus == "Up"){
                    $('#status'+data.data[i].ip.replace(/\./g,"-")).html('<font color="Lime">'+data.data[i].checkstatus+'</font>');
                } else if(data.data[i].checkstatus == "SSHOK"){
                    $('#status'+data.data[i].ip.replace(/\./g,"-")).html('<font color="#FF9900">'+data.data[i].checkstatus+'</font>');
                } else {
                    $('#status'+data.data[i].ip.replace(/\./g,"-")).html('<font color="red">'+data.data[i].checkstatus+'</font>');
                }
                $('#UpTime'+data.data[i].ip.replace(/\./g,"-")).html(data.data[i].checktime);
                $('#commitID'+data.data[i].ip.replace(/\./g,"-")).html(data.data[i].commitid);
                $('#Tag'+data.data[i].ip.replace(/\./g,"-")).html(data.data[i].updatetime);
            }

        }
    });

};


//function push_edit_host_table(p){
//    var param={ project:p};
//    $.getJSON('/hostlist', param,  function(data){
//        var htm=['<table class="table table-hover">'];
//
//        htm.push('<thead><tr><th>hostname</th><th>ip</th><th>pnum</th><th>project</th></tr></thead>');
//        $.each(data, function(ip, data){
//            if(data[0] != "essExpansion"){
//                htm.push('<tr>');
//                htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="hostname" value="'+data[0]+'">'+'</td>');
//                htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_git" placeholder="ip" value="'+ip+'">'+'</td>');
//                htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="pnum" value="'+data[1]+'">'+'</td>');
//                htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_git" placeholder="project" value="'+data[2]+'">'+'</td>');
//                htm.push('</tr>');
//            }
//        })
//        htm.push('<tr><td><button id="edit_host" class="btn btn-small btn-danger" project="'+p+'" >更新主机信息</button></td></tr>');
//        htm.push('</table>');
//        $('#add_host_table').html(htm.join(''));
//
//    });
//};


function parseQuery(searchStr) {
    var search = searchStr || location.search.slice(1)
    var searchObj = {}
    search.split('&').forEach(function(param) {
        var paramArr = param.split('=')
        var k = paramArr[0]
        var v = paramArr[1]
        searchObj[k] = v
    })
    return searchObj
}

function addQuery(href, key, value) {
    var hrefArr = href.split('?')
    var url = hrefArr[0]
    var search = hrefArr[1] || ''
    var newSearchArr = []
    search.split('&').forEach(function(param) {
        var paramArr = param.split('=')
        var k = paramArr[0]
        if(k !== key) {
            newSearchArr.push(param)
        }
    })
    newSearchArr.push(key + '=' + value)
    return url + '?' + newSearchArr.filter(s => s !== '').join('&')
}


$("body").on('click', '.host_list', function(){
    var p = $(this).attr('data-project')
    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })
    host_list_push(p)
});

function host_list_argv(p){

    host_list_push(avgr['project'])
}

function host_list_push(p){

    $('p').css('background','');
    $($('[data-project="'+p+'"]').find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    //host_list_table(p)
    online_tag(p)
    current_tag(p)
    get_svcadd(p)

    var htm1=['<input type="hidden" name="project" id="ipt_project" value="'+p+'" />'];
    $('#select_project').html(htm1.join(''));

    var htm3=['<a href="javascript:;" class="project_info_table" status="close" onclick=\'push_project_manage("'+p+'");\'>项目信息:'+p+'</a>'];
    $('#project_button').html(htm3.join(''));

    var htm6=['<p>'+'上线管理:    '+p+'</p>'];
    $('#onlineManage').html(htm6.join(''));

    if(p.split("_",1) == "online"){
        var htm5=['<button id="btn_submit" class="btn btn-warning" type="button">'+p.split("_",1)+'更新</button>'];
    }else{
        var htm5=['<button id="btn_submit" class="btn btn-success" type="button">'+p.split("_",1)+'更新</button>'];
    }

    $('#updatebutton').html(htm5.join(''));

    $('#ProgressBarDiv').html('');
    $('#cnt').html("");
    $('#resDiv').html("");
    $('#add_host_table').html("");
    $('#hostManage').html("");
    $('#hostManage').attr('status','close')
    $('#project_div').html("");
    $('#project_div').attr('status','close');
    $('#config_div').html("");
    $('#config_div').attr('status','close');

    //clearInterval(timeout);

    //if(timeout1){clearInterval(timeout1)};
    //    timeout1 = setInterval(function(){
    //        host_list_status(p);
    //},10000);

}


$("body").on('click', '.host_list_admin', function(){
    $('p').css('background','');
    $($(this).find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    var p = $(this).attr('data-project')

    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })

    //host_list_table(p)

    var htm1=['<input type="hidden" name="project" id="ipt_project" value="'+p+'" />'];
    $('#select_project').html(htm1.join(''));

    $('#ProgressBarDiv').html('');
    $('#cnt').html("");
    $('#resDiv').html("");
    $('#add_host_table').html("");
    $('#hostManage').html("");
    $('#hostManage').attr('status','close')
    $('#project_div').html("");
    $('#project_div').attr('status','close');
    //push_add_host_table(p)
});


function selectAll(n){
    var a = document.getElementsByName(n);
    if(typeof(a[0]) != 'undefined'){
        if(a[0].checked){
            for(var i=0; i<a.length; i++){
                if (a[i].name == n) a[i].checked = false;
            }
        }else{
            for(var i=0; i<a.length; i++){
                if (a[i].name == n) a[i].checked = true;
            }
        }
    }
}


function next(taskid, num){
    var param={ taskid: taskid };
    $.getJSON('/cmdreturns', param,  function(data){
        var percentage=parseInt(data['progress'] * 100 / num);
        if(percentage<10){
            var percentage=10;
        }

        var ProgressBar='<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        var ProgressBarDanger='<div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        $('#ProgressBarDiv').html(ProgressBar);

        if(data['progress'] == num){
            clearInterval(timeout);
        }

        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>状态</th><th>执行过程</th></tr>');
            htm.push('<tr>');
            if(data['status'] == 'ok' ){
               htm.push('<td class="success">'+data['status']+'</td>');
            }else if(data['status'] == 'wait'){
               htm.push('<td class="success">'+data['status']+'</td>');
            }else{
               htm.push('<td class="danger">'+data['status']+'</td>');
               $('#ProgressBarDiv').html(ProgressBarDanger);
               clearInterval(timeout);
            }
            htm.push('<td><div contenteditable="true">'+data['result']+'</div></td>');
            htm.push('</tr>');
        htm.push('</table>');
        $('#cnt').html(htm.join(''));
    });
};

function hostlisterrweb(){

    $.getJSON('/hostlisterr', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>project</th><th>hostname</th><th>ip</th><th>status</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function postlist(){

    $.getJSON('/port_list', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>port</th><th>project</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function projectall(){

    $.getJSON('/project_list', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>group</th><th>project</th><th>port</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            //htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td><a href="/online?group='+data[i][0]+'&project='+data[i][1]+'" target="_blank">'+data[i][1]+'</a></td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function online_log_time(p){
    var param={ project:p };
    $.getJSON('/online_log_time', param, function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
};


$("body").on('click', '.online_log_time', function(){
    $('p').css('background','');
    $($(this).find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    var p = $(this).attr('data-project')

    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })

    var param={ project:p };
    $.getJSON('/online_log_time', param, function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
});

function online_log_all(){

    $.getJSON('/online_log_all', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
};

function online_log_info(id){
    var param={ taskid:id };
    $.getJSON('/cmdreturns', param,  function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>状态</th><th>执行过程</th></tr>');
        htm.push('<tr>');
        if(data['status'] == 'ok' ){
           htm.push('<td class="success">'+data['status']+'</td>');
        }else{
           htm.push('<td class="danger">'+data['status']+'</td>');
        }
        htm.push('<td><div contenteditable="true">'+data['result']+'</div></td>');
        htm.push('</tr>');
        htm.push('</table>');
        $('#online_log').html(htm.join(''));
    });
};


//function getLocalTime(nS) {
//    return new Date(parseInt(nS) * 1000 ).toLocaleString()
//}


function add0(m){return m<10?'0'+m:m }


function getLocalTime(nS) {
    var date=new Date(parseInt(nS)* 1000);
    var year=date.getFullYear();
    var mon = date.getMonth()+1;
    var day = date.getDate();
    var hours = date.getHours();
    var minu = date.getMinutes();
    var sec = date.getSeconds();

    return year+'-'+add0(mon)+'-'+add0(day)+' '+add0(hours)+':'+add0(minu)+':'+add0(sec);
}



function push_project_info(p){
    var param={ project:p};
    $.getJSON('/project_info_json', param, function(data){
        if(data.status == 'fail'){
            alert(data.status+":  "+data.log);
            return false;
        }

    $.getJSON('/group_list', function(groupdata){
    $.getJSON('/codetype_list_all', function(codetypedata){
    $.getJSON('/environment_list_all', function(environmentdata){
    $.getJSON('/get_projectk8sclustername', param, function(k8smanagenamedata){
        
        var htm=['<table class="table table-hover ">'];

        htm.push('<tr>');
        htm.push('<td width="120" align="right">project:</td>');
        htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_project" value="'+data.data.project+'">'+'</td>');
        htm.push('<td>带环境的项目名,全局唯一 $project$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">group:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_group">');
        for(var i=0,len=groupdata.length; i<len; i++){
            if(groupdata[i] == data.data.group){
                htm.push('<option value="'+groupdata[i]+'" selected="selected">'+groupdata[i]+'</option>');
            }else{
                htm.push('<option value="'+groupdata[i]+'">'+groupdata[i]+'</option>');
            }
        }
        htm.push('</select></td>');
        htm.push('<td>选择分组 $group$</td>');
        htm.push('</tr>');


        htm.push('<tr>');
        htm.push('<td width="120" align="right">environment:</td>');
        htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_environment" placeholder="test" value="'+data.data.environment+'">'+'</td>');
        htm.push('<td>环境,不可改变 $environment$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">k8scluster:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_k8smanagename">');
        for(var i=0,len=k8smanagenamedata.data.length; i<len; i++){
            if(k8smanagenamedata.data[i] == data.data.k8smanagename){
                htm.push('<option value="'+k8smanagenamedata.data[i]+'" selected="selected">'+k8smanagenamedata.data[i]+'</option>');
            }else{
                htm.push('<option value="'+k8smanagenamedata.data[i]+'">'+k8smanagenamedata.data[i]+'</option>');
            }
        }
        htm.push('</select></td>');
        htm.push('<td>选择k8s集群</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">k8s-namespace:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_namespace" placeholder="default" value="'+data.data.namespace+'">'+'</td>');
        htm.push('<td>发布pod到k8s集群的指定namespace</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">codetype:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_codetype">');
        for(var i=0,len=codetypedata.length; i<len; i++){
            if(codetypedata[i] == data.data.codetype){
                htm.push('<option value="'+codetypedata[i]+'" selected="selected">'+codetypedata[i]+'</option>');
            }else{
                htm.push('<option value="'+codetypedata[i]+'">'+codetypedata[i]+'</option>');
            }
        }
        htm.push('</select></td>');
        htm.push('<td>代码类型,不建议修改,初次添加项目已关联模板,模板不会改变</td>');
        htm.push('</tr>');


        htm.push('<tr>');
        htm.push('<td width="120" align="right">projectName:</td>');
        htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_p" value="'+data.data.p+'">'+'</td>');
        htm.push('<td>项目名,不可修改,新加可以克隆项目 $p$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">git:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="git://github.com/sre/op.git" value="'+data.data.git+'">'+'</td>');
        htm.push('<td>git协议的git仓库地址,可修改</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">branch:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_branch" placeholder="python" value="'+data.data.branch+'">'+'</td>');
        htm.push('<td>git分支,可修改</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">port:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_port" placeholder="go port[8000-10000]  python port[3000-5000]" value="'+data.data.port+'">'+'</td>');
        htm.push('<td>docker内部进程启动的默认监听端口 $branch$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">nodeport:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_nodeport" placeholder="30000-50000" value="'+data.data.nodeport+'">'+'</td>');
        htm.push('<td>k8s集群外部调用端口,默认自动生成 $nodeport$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">makepath:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_makepath" placeholder="codepath" value="'+data.data.makepath+'">'+'</td>');
        htm.push('<td>编译代码的目录 $makepath$</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">make:</td>');
        htm.push('<td><textarea id="add_make" rows="5" cols="100"  >'+data.data.make+'</textarea></td>');
        htm.push('<td>编译操作(根据模板生成,项目可以单独调整)</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">config(name=subPath):</td>');
        htm.push('<td><textarea id="add_config" rows="5" cols="100"  >'+data.data.config+'</textarea></td>');
        htm.push('<td>配置文件,名字会自动生成yaml中subPath对应的配置文件名</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">start:</td>');
        htm.push('<td><textarea id="add_start" rows="5" cols="100"  >'+data.data.start+'</textarea></td>');
        htm.push('<td>启动脚本start.sh内容(根据模板生成,项目可以单独调整)</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">dockerfile:</td>');
        htm.push('<td><textarea id="add_dockerfile" rows="5" cols="100"  >'+data.data.dockerfile+'</textarea></td>');
        htm.push('<td>Dockerfile文件内容,打包镜像(根据模板生成,项目可以单独调整)</td>');
        htm.push('</tr>');
        
        htm.push('<tr>');
        htm.push('<td width="120" align="right">k8syaml:</td>');
        htm.push('<td><textarea id="add_k8syaml" rows="5" cols="100"  >'+data.data.k8syaml+'</textarea></td>');
        htm.push('<td>发布pod的yaml文件(根据模板生成,项目可以单独调整)</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">remarks:</td>');
        htm.push('<td><textarea id="add_remarks" rows="5" cols="100"  >'+data.data.remarks+'</textarea></td>');
        htm.push('<td>备注</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td><div><div style="float:left"><button id="update_project" class="btn btn-small btn-success" >确认修改</button></div><div style="float:right"><button id="del_project" class="btn btn-small btn-danger">删除项目及关联的应用</button></div></div></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right"></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('<tr class="success">');
        htm.push('<td width="120" align="right">克隆新项目</td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">新项目环境:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_cloneenvironment">');
        for(var i=0,len=environmentdata.length; i<len; i++){
            if(environmentdata[i] == data.data.environment){
                htm.push('<option value="'+environmentdata[i]+'" selected="selected">'+environmentdata[i]+'</option>');
            }else{
                htm.push('<option value="'+environmentdata[i]+'">'+environmentdata[i]+'</option>');
            }
        }
        htm.push('</select></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">新项目名称:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_clonep" value="'+data.data.p+'">'+'</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td><div><div style="float:left"><button id="clone_project" class="btn btn-small btn-success" >克隆新项目</button></div><div style="float:right"></div></div></td>');
        htm.push('</tr>');

        htm.push('</table>');
        $('#project_div').html(htm.join(''));

    })
    })
    })
    })
    });
};


$("body").on('click', '#clone_project', function(){
    if (confirm('请确认克隆项目名称,不会冲突')) {
        var add_project          = $('#add_project').val()
        var add_newenvironment   = $('#add_cloneenvironment').val()
        var add_newp             = $('#add_clonep').val()
        var newproject = add_newenvironment + '_' +  add_newp
        if(newproject == add_project){
            alert('ERROR: project name conflict');
            return false;
        }
        if(!add_newenvironment){
            alert('new environment null');
            return false;
        }
        if(!add_project){
            alert('new project name null');
            return false;
        }
        var param = {
            project: add_project,
            environment: add_newenvironment,
            p: add_newp
        }
        $.post('/clone_project', param, function(data){
            project_list()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


function push_project_manage(p){
    var status = $('#project_div').attr('status')
    if (status == 'close') {
        push_project_info(p)
        //hostmanage_list_table(p)
        //push_add_host_table(p)

        $('#project_div').attr('status','open')
    }else{
        $('#project_div').html("");
        $('#config_div').html("");
        $('#hostManage').html("");
        $('#add_host_table').html("");
        $('#project_div').attr('status','close')
    }
};



$("#rmpod").on('click', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };
        if (confirm('警告:请确认删除当前pod '+ p +'?')) {
            $.post('/rmpod', param, function(data){
                alert('delete pod ' + p + ' ' + data.status + ':' + data.log);
            }, 'json');
        };
    }
    else{
        alert('project null');
    };
});

$("#rmlock").on('click', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };

        $.getJSON('/rmpkl', param, function(data){
            alert(p + ' lock clear done!');
        });
    }
    else{
        alert('project null');
    };
});

$("#killtask").on('click', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };
        if (confirm('警告:请确认终止当前任务 '+ p +'?')) {
            $.getJSON('/killtask', param, function(data){
                alert('kill task ' + p + ' ' + data.status + ':' + data.log);
            });
        };
    }
    else{
        alert('project null');
    };
});

function push_codetypemanage(){
    $.getJSON('/codetype_list_all', function(codetypedata){

        var htm=['<table class="table table-hover ">'];

        htm.push('<tr>');
        htm.push('<td width="120" align="right">选择代码类型:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_codetypemanage">');
        for(var i=0,len=codetypedata.length; i<len; i++){
            htm.push('<option value="'+codetypedata[i]+'">'+codetypedata[i]+'</option>');
        }
        htm.push('</select></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="180" align="right">选择模板文件:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_templatefilename"><option value="make" selected = "selected">make (编译脚本内容)</option><option value="start">start (启动脚本)</option><option value="Dockerfile">Dockerfile (打包镜像)</option><option value="podyaml">podyaml (k8s的pod启动yaml模板文件)</option></select>'+'</td>');
        htm.push('</tr>');
    
    
        htm.push('<tr>');
        htm.push('<td width="180" align="right">是否使用自定义模板文件名:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_templatefilecustom"><option value="yes">yes (使用自定义模板文件)</option><option value="no" selected = "selected">no (添加内置模板文件)</option></select>'+'</td>');
        htm.push('</tr>');



        htm.push('<tr>');
        htm.push('<td width="120" align="right">自定义模板文件名:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_codetypemanagefilename" placeholder="自定义模板文件名" value="">'+'</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">模板文件内容:</td>');
        htm.push('<td><textarea id="add_codetypemanagefilecontent" rows="5" cols="100"  ></textarea></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">模板文件变量列表说明:</td>');
        htm.push('<td><textarea id="" rows="11" cols="100" readonly="readonly" >');
        htm.push('$project$ : 环境_项目名称 (发布系统内项目唯一标识名称)&#10;');
        htm.push('$p$ : 项目名称(可多环境同名)&#10;');
        htm.push('$group$ : 项目组&#10;');
        htm.push('$environment$ : 环境&#10;');
        htm.push('$codetype$ : 代码类型&#10;');
        htm.push('$branch$ : 代码仓库分支&#10;');
        htm.push('$path$ : 拉取后的代码仓库目录,用于编译打包的绝对路径&#10;');
        htm.push('$makepath$ : 在代码仓库中,进入到目录后进行编译&#10;');
        htm.push('$port$ : pod容器端口&#10;');
        htm.push('$nodeport$ : 外部暴露访问端口&#10;');
        htm.push('$dockerurl$ : docker image 仓库地址url&#10;');
        htm.push('$k8snodeip1$ : k8s集群第一个节点ip&#10;');
        htm.push('$k8snode1$ : k8s集群第一个节点主机名&#10;');
        htm.push('</textarea></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td><div><div style="float:left"><button id="add_templatefile" class="btn btn-small btn-success" >添加模板文件</button></div><div style="float:right"></div></div></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right"></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right"><a href="javascript:;" class="templatefile_info_table" status="close" onclick=\'templatefile_all();\'>模板列表:</a></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('</table>');
        $('#codetypemanage_button_div').html(htm.join(''));

    });
};

$("body").on('click', '#add_templatefile', function(){

    var add_templatefilecustom              = $('#add_templatefilecustom').val()
    if (add_templatefilecustom == 'yes') {
        var add_codetypemanagefilename      = $('#add_codetypemanagefilename').val()
    }else{
        var add_codetypemanagefilename      = $('#add_templatefilename').val()
    }

    var add_codetypemanage              = $('#add_codetypemanage').val()
    var add_codetypemanagefilecontent   = $('#add_codetypemanagefilecontent').val()

    if(!add_codetypemanage){
        alert('codetype null');
        return false;
    }
    if(!add_codetypemanagefilename){
        alert('codetype filename null');
        return false;
    }

    var param = {
        codetypemanage: add_codetypemanage,
        codetypemanagefilename: add_codetypemanagefilename,
        codetypemanagefilecontent: add_codetypemanagefilecontent
    }
    $.post('/add_templatefile', param, function(data){
        push_templatefile_all()
        alert(data.status+"  "+data.log);
    }, 'json');

});


function templatefile_all(){
    var status = $('#templatefile_list_button_div').attr('status')
    if (status == 'close') {
        push_templatefile_all()
        $('#templatefile_list_button_div').attr('status','open')
    }else{
        $('#templatefile_list_button_div').html("");
        $('#templatefile_list_button_div').attr('status','close')
    }
};

function k8scluster_all(){
    var status = $('#k8smanage_list_button_div').attr('status')
    if (status == 'close') {
        push_k8scluster_all()
        $('#k8smanage_list_button_div').attr('status','open')
    }else{
        $('#k8smanage_list_button_div').html("");
        $('#k8smanage_list_button_div').attr('status','close')
    }
};

function push_templatefile_all(){
    $.getJSON('/get_templatefile_all', function(data){
        var htm=['<table class="table table-hover ">'];
        htm.push('<thead><tr><th>更新</th><th>代码类型</th><th>文件名</th><th>模板文件内容</th><th>删除</th></thead>');
        for(var i=0,len=data.data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td width="30"><button class="btn btn-small btn-success" id="up_templatefile"  codetype="'+data.data[i].codetype+'" templatefilename="'+data.data[i].templatefilename+'" i="'+i+'" >更新</button></td>');
            htm.push('<td width="120">'+'<input type="text" readOnly="true" class="form-control" id="codetype'+i+'" value="'+data.data[i].codetype+'">'+'</td>');
            htm.push('<td width="120">'+'<input type="text" readOnly="true" class="form-control" id="templatefilename'+i+'" value="'+data.data[i].templatefilename+'">'+'</td>');
            htm.push('<td width="400">'+'<textarea rows="5" cols="100" id="templatefilecontent'+i+'">'+data.data[i].templatefilecontent+'</textarea></td>');
            htm.push('<td width="30"><button class="btn btn-small btn-danger"  id="del_templatefile" codetype="'+data.data[i].codetype+'" templatefilename="'+data.data[i].templatefilename+'" i="'+i+'" >删除</button></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#templatefile_list_button_div').html(htm.join(''));
    });
}

function push_k8scluster_all(){
    $.getJSON('/get_k8scluster_all', function(data){
        var htm=['<table class="table table-hover ">'];
        htm.push('<thead><tr><th>更新</th><th>环境</th><th>k8s集群名称</th><th>k8s集群管理文件内容</th><th>删除</th></thead>');
        for(var i=0,len=data.data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td width="30"><button class="btn btn-small btn-success" id="up_k8scluster"  environment="'+data.data[i].environment+'" k8smanagename="'+data.data[i].k8smanagename+'" i="'+i+'" >更新</button></td>');
            htm.push('<td width="120">'+'<input type="text" readOnly="true" class="form-control" id="environment'+i+'" value="'+data.data[i].environment+'">'+'</td>');
            htm.push('<td width="120">'+'<input type="text" readOnly="true" class="form-control" id="k8smanagename'+i+'" value="'+data.data[i].k8smanagename+'">'+'</td>');
            htm.push('<td width="400">'+'<textarea rows="5" cols="100" id="k8smanagefilecontent'+i+'">'+data.data[i].k8smanagefilecontent+'</textarea></td>');
            htm.push('<td width="30"><button class="btn btn-small btn-danger"  id="del_k8scluster" environment="'+data.data[i].environment+'" k8smanagename="'+data.data[i].k8smanagename+'" i="'+i+'" >删除</button></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#k8smanage_list_button_div').html(htm.join(''));
    });
}



function push_k8smanage(){
    $.getJSON('/environment_list_all', function(environmentdata){

        var htm=['<table class="table table-hover ">'];

        htm.push('<tr>');
        htm.push('<td width="120" align="right">选择环境类型:</td>');
        htm.push('<td>'+'<select class="form-control" id="add_k8smanageenvironment">');
        for(var i=0,len=environmentdata.length; i<len; i++){
            htm.push('<option value="'+environmentdata[i]+'">'+environmentdata[i]+'</option>');
        }
        htm.push('</select></td>');
        htm.push('<td>选择哪个集群可以使用此集群</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">k8s集群名称:</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_k8smanagename" placeholder="k8s集群名称" value="">'+'</td>');
        htm.push('<td>集群自定义名称</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right">管理文件内容:</td>');
        htm.push('<td><textarea id="add_k8smanagefilecontent" rows="5" cols="100"  ></textarea></td>');
        htm.push('<td>默认/etc/kubernetes/admin.conf文件内容.管理文件中server: 发布系统必须可连通,不要填主机名</td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td><div><div style="float:left"><button id="add_k8scluster" class="btn btn-small btn-success" >添加k8s集群</button></div><div style="float:right"></div></div></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right"></td>');
        htm.push('<td></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('<tr>');
        htm.push('<td width="120" align="right"><a href="javascript:;" class="k8scluster_info_table" status="close" onclick=\'k8scluster_all();\'>k8s集群列表:</a></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        htm.push('</table>');
        $('#k8smanage_button_div').html(htm.join(''));

    });
};


$("body").on('click', '#add_k8scluster', function(){

    var add_k8smanageenvironment     = $('#add_k8smanageenvironment').val()
    var add_k8smanagename            = $('#add_k8smanagename').val()
    var add_k8smanagefilecontent     = $('#add_k8smanagefilecontent').val()

    if(!add_k8smanageenvironment){
        alert('k8s manage environment null');
        return false;
    }
    if(!add_k8smanagename){
        alert('k8s manage name null');
        return false;
    }
    if(!add_k8smanagefilecontent){
        alert('k8s manage file null');
        return false;
    }
    var param = {
        k8smanageenvironment: add_k8smanageenvironment,
        k8smanagename: add_k8smanagename,
        k8smanagefilecontent: add_k8smanagefilecontent
    }
    $.post('/add_k8scluster', param, function(data){
        push_k8scluster_all()
        alert(data.status+"  "+data.log);
    }, 'json');

});


$("body").on('click', '#del_templatefile', function(){
    var codetype = $(this).attr('codetype')
    var templatefilename = $(this).attr('templatefilename')
    if (confirm('请确认删除: '+codetype+'  '+templatefilename)) {
        var param = {
            codetype:    codetype,
            templatefilename: templatefilename,
        }
        $.post('/del_templatefile', param, function(data){
            push_templatefile_all()
            alert('delete '+codetype+'  '+templatefilename+': '+ data['status']);
        }, 'json');
    }
});


$("body").on('click', '#up_templatefile', function(){
    var num = $(this).attr('i')
    var codetype = $(this).attr('codetype')
    var templatefilename = $(this).attr('templatefilename')
    var templatefilecontent = $('#templatefilecontent'+num).val()

    if (confirm('请确认更新: '+codetype+'  '+templatefilename)) {
        var param = {
            codetype:    codetype,
            templatefilename:  templatefilename,
            templatefilecontent:   templatefilecontent
        }
        $.post('/update_templatefile', param, function(data){
            alert('update '+codetype+'  '+templatefilename+': '+ data['status']);
        }, 'json');
    }
});

$("body").on('click', '#del_k8scluster', function(){
    var environment = $(this).attr('environment')
    var k8smanagename = $(this).attr('k8smanagename')
    if (confirm('请确认删除: '+environment+'  '+k8smanagename)) {
        var param = {
            environment:    environment,
            k8smanagename: k8smanagename,
        }
        $.post('/del_k8scluster', param, function(data){
            push_k8scluster_all()
            alert('delete '+environment+'  '+k8smanagename+': '+ data['status']);
        }, 'json');
    }
});

$("body").on('click', '#up_k8scluster', function(){
    var num = $(this).attr('i')
    var environment = $(this).attr('environment')
    var k8smanagename = $(this).attr('k8smanagename')
    var k8smanagefilecontent = $('#k8smanagefilecontent'+num).val()

    if (confirm('请确认更新: '+environment+'  '+k8smanagename)) {
        var param = {
            environment:    environment,
            k8smanagename:  k8smanagename,
            k8smanagefilecontent:   k8smanagefilecontent
        }
        $.post('/update_k8scluster', param, function(data){
            alert('update '+environment+'  '+k8smanagename+': '+ data['status']+' : '+data['log']);
        }, 'json');
    }
});


$("body").on('click', '#clean_git_cache', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };

        $.getJSON('/clean_git_cache', param, function(data){
            alert(p + ' git cache clear done!' + data);
        });
    }
    else{
        alert('project null');
    };
});


function online_tag(p){
    var param = {
        project: p
    }
    $.getJSON('/online_tag', param, function(data){
        var htm=['<select id="select_tag" class="form-control">'];
        if(data.length == 0){
            htm.push('<option value="null">null update</option>');
        }
        else{
            for(var i=0,len=data.length; i<len; i++){
                htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
            }
        }
        htm.push('</select>');
        $('#tag_div').html(htm.join(''));
    });
};

function get_svcadd(p){
    var param = {
        project: p
    }
    $.getJSON('/get_svcadd', param, function(data){
        var htm=['<table class="table table-hover" >'];
        //var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr>');
        htm.push('<td>服务访问地址:</td>');
        htm.push('<td>');
        htm.push('<a href="http://'+data.data.url+'" target="_blank">http://'+data.data.url+'</a>');
        htm.push('</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td>Service地址(同namespace调用):</td>');
        htm.push('<td>'+data.data.svc+'</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td>Service地址(不同namespace调用地址):</td>');
        htm.push('<td>'+data.data.svc_ns+'</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td>镜像地址tag(最后打包成功):</td>');
        htm.push('<td>'+data.data.img+'</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td>镜像地址latest:</td>');
        htm.push('<td>'+data.data.img_latest+'</td>');
        htm.push('</tr>');
        htm.push('</table>');
        $('#svcadddiv').html(htm.join(''));
    });
};


function current_tag(p){
    var param = {
        project: p
    }
    $.getJSON('/current_tag', param, function(data){
        $('#online_tag_div').html(data[0]);
    });
};




$("#lastlog").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p == undefined){
        alert('project null');
    }
    var param={ project:p };
    $.getJSON('/lock_check', param, function(lockdata){
        if(lockdata['status'] == "ok"){
            var percentage=100;
        }else{
            var percentage=50;
        }
        var ProgressBar='<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';
        var ProgressBarDanger='<div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        $.getJSON('/lastlog', param,  function(data){
            var htm=['<table class="table table-bordered">'];
            htm.push('<tr><th>状态</th><th>执行过程</th></tr>');
            var status=''
            htm.push('<tr>');
            if(data['status'] == 'fail' ){
               var status=data['status']
               htm.push('<td class="danger">'+data['status']+'</td>');
               clearInterval(timeout);
            }else{
               htm.push('<td class="success">'+data['status']+'</td>');
            }
            htm.push('<td><div contenteditable="true">'+data['result']+'</div></td>');
            htm.push('</tr>');
            htm.push('</table>');
            if(status == 'fail'){
                $('#ProgressBarDiv').html(ProgressBarDanger);
                //clearInterval(timeout);
                alert('严重警告：注意看错误，上线失败了！！！')
            } else {
                $('#ProgressBarDiv').html(ProgressBar);
            }
            $('#cnt').html(htm.join(''));
        });
    });
});


function online_statistics(){
    $.getJSON('/online_statistics', function(data){
        var htm=['<table class="table table-hover" border="2">'];


        htm.push('<tr><td rowspan="2"><h5>project</h5></td><td colspan="3"><h5>前1周</h5></td><td colspan="3"><h5>前2周</h5></td><td colspan="3"><h5>前3周</h5></td><td colspan="3"><h5>前4周</h5></td></tr>');

        htm.push('<tr><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td></tr>');

        $.each(data, function(i, h){
            htm.push('<tr>');
            htm.push('<td>'+i+'</td>');
            htm.push('<td>'+h[0]+'</td>');
            htm.push('<td>'+h[1]+'</td>');
            htm.push('<td>'+h[2]+'</td>');
            htm.push('<td>'+h[3]+'</td>');
            htm.push('<td>'+h[4]+'</td>');
            htm.push('<td>'+h[5]+'</td>');
            htm.push('<td>'+h[6]+'</td>');
            htm.push('<td>'+h[7]+'</td>');
            htm.push('<td>'+h[8]+'</td>');
            htm.push('<td>'+h[9]+'</td>');
            htm.push('<td>'+h[10]+'</td>');
            htm.push('<td>'+h[11]+'</td>');
            htm.push('</tr>');

        })

        htm.push('</table>');
        $('#statistics').html(htm.join(''));
    })
};

function cmslog(){
    $.getJSON('/cmslog', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr><td><h5>@timestamp</h5></td><td><h5>auth_name</h5></td><td><h5>method</h5></td><td><h5>status</h5></td><td><h5>request_api</h5></td><td><h5>remote_addr</h5></td><td><h5>request_time</h5></td></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            for(var u=0,len1=data[i].length; u<len1; u++){
                if(u==0){
                    var DataTime = getLocalTime(data[i][0])
                    htm.push('<td>'+DataTime+'</td>');
                }else{
                    htm.push('<td>'+data[i][u]+'</td>');
                }
            }
            htm.push('</tr>');
        }

        htm.push('</table>');
        $('#cms_log').html(htm.join(''));
    })
};


function erplog(){
    $.getJSON('/erplog', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr><td><h5>@timestamp</h5></td><td><h5>auth_name</h5></td><td><h5>method</h5></td><td><h5>status</h5></td><td><h5>request_api</h5></td><td><h5>parameter</h5></td><td><h5>description</h5></td><td><h5>error_message</h5></td><td><h5>platform</h5></td></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            for(var u=0,len1=data[i].length; u<len1; u++){
                if(u==0){
                    var DataTime = getLocalTime(data[i][0])
                    htm.push('<td>'+DataTime+'</td>');
                }else{
                    htm.push('<td>'+data[i][u]+'</td>');
                }
            }
            htm.push('</tr>');
        }

        htm.push('</table>');
        $('#erp_log').html(htm.join(''));
    })
};


function stop_submit(ip){
    var p = $('#ipt_project').val()
    if (p != undefined){
        if (confirm('请确认停止服务'+ p +'!')) {
            var param = {
                operation: 'serviceStop',
                project: p,
                client: ip,
            };
            updateonline(param)
        };
    }
    else{
        alert('project null');
    };
};


function stopserver(param){

    $.post('/stopserver', param, function(data){
        $("#resDiv").html( "&nbsp;&nbsp;&nbsp;&nbsp;operation:&nbsp;&nbsp;"+data.operation+"<br>&nbsp;&nbsp;&nbsp;&nbsp;taskid:&nbsp;&nbsp;"+data.taskid+"<br>&nbsp;&nbsp;&nbsp;&nbsp;logout:&nbsp;&nbsp;"+data.output+"<br>&nbsp;&nbsp;&nbsp;&nbsp;hostlist:&nbsp;&nbsp;"+data.host+"<br>&nbsp;&nbsp;&nbsp;&nbsp;tag:&nbsp;&nbsp;"+data.tag+"<br>&nbsp;&nbsp;&nbsp;&nbsp;project:&nbsp;&nbsp;"+data.project);
        if(timeout){clearInterval(timeout)};
        timeout = setInterval(function(){
            next(data.taskid, 1);
        },4000);
        $('#cnt').html("");
    }, 'json');
};


function workorder_group_list(){
    $.getJSON('/group_list', function(data){
        var htm=['<select class="form-control" id="selectgroup" onchange="workorder_project_list()">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#group').html(htm.join(''));
        workorder_project_list();
    })
};


function workorder_project_list(){

    var selectgroup = $('#selectgroup').val()
    var param = {
        group: selectgroup,
        functype: 'workorder'
    }

    $.getJSON('/project', param , function(data){
        var htm=['<select class="form-control" id="selectproject">'];
        $.each(data, function(g, projectlist){
            var h=projectlist.sort();
            for(var i=0,len=h.length; i<len; i++){
                if(h[i].indexOf("online_")>-1){
                    htm.push('<option value="'+h[i]+'">'+h[i]+'</option>');
                }
            }
        })
        htm.push('</select>');
        $('#project').html(htm.join(''));
    });
};


$("body").on('click', '.workordermenu', function(){
    var menu = $(this).attr('menu');
    //userservicegrouplist(username)
    selectworkmenu(menu)
});


function selectworkmenu(menu){
    if(menu == 'createworkorder'){
        createworkorder()
        workorder_group_list()

    } else if(menu == 'waitworkorder'){
        waitworkorder()
    } else if(menu == 'doneworkorder'){
        doneworkorder()
    }
};

function createworkorder(){
    var htm=['<table class="table table-hover" border="2">'];
    htm.push('<tr>');
    htm.push('<td>group:</td>');
    htm.push('<td><div id="group"></div></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td>project:</td>');
    htm.push('<td><div id="project"></div></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td>remarks:</td>');
    htm.push('<td><textarea id="remarks" rows="5" cols="100"></textarea></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td></td>');
    htm.push('<td><button id="subworkorder" class="btn btn-small btn-success">提交工单</button></td>');
    htm.push('</tr>');
    htm.push('</table>');

    $('#workorder_div').html(htm.join(''));
}
function waitworkorder(){
    $.getJSON('/wait_workorder', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr>');
        htm.push('<td>组</td>');
        htm.push('<td>项目</td>');
        htm.push('<td>申请人</td>');
        htm.push('<td>申请时间</td>');
        htm.push('<td>状态</td>');
        //htm.push('<td>执行人</td>');
        //htm.push('<td>完成时间</td>');
        htm.push('<td>关闭工单</td>');
        htm.push('<td>备注</td>');
        htm.push('</tr>');

        for(var i=0,len=data.length; i<len; i++){
            var applicationtime = getLocalTime(data[i][3])
            //var completiontime = getLocalTime(data[i][6])
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td><a href="/online?group='+data[i][0]+'&project='+data[i][1]+'" target="_blank">'+data[i][1]+'</a></td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+applicationtime+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            //htm.push('<td>'+data[i][5]+'</td>');
            //htm.push('<td>'+data[i][6]+'</td>');
            htm.push('<td><button id="downworkorder" time="'+data[i][3]+'" class="btn btn-small btn-success">关闭工单</button></td>');
            htm.push('<td><textarea id="remarks" rows="3" cols="40">'+data[i][7]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#workorder_div').html(htm.join(''));
    })

}
function doneworkorder(){
    $.getJSON('/done_workorder', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr>');
        htm.push('<td>组</td>');
        htm.push('<td>项目</td>');
        htm.push('<td>申请人</td>');
        htm.push('<td>申请时间</td>');
        htm.push('<td>状态</td>');
        htm.push('<td>执行人</td>');
        htm.push('<td>完成时间</td>');
        htm.push('<td>备注</td>');
        htm.push('</tr>');
        for(var i=0,len=data.length; i<len; i++){
            var applicationtime = getLocalTime(data[i][3])
            var completiontime = getLocalTime(data[i][6])

            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+applicationtime+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('<td>'+completiontime+'</td>');
            htm.push('<td><textarea id="remarks" rows="2" cols="25">'+data[i][7]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#workorder_div').html(htm.join(''));
    })
}


$("body").on('click', '#subworkorder', function(){
    if (confirm('请确认提交工单信息')) {
        var group   = $('#selectgroup').val()
        var project = $('#selectproject').val()
        var remarks = $('#remarks').val()
        if (project != undefined){
            var param = {
                group:    group,
                project:  project,
                remarks:  remarks,
            };
            $.post('/add_workorder', param, function(data){
                alert(data.status+"  "+data.log);
            }, 'json');
        }
        else{
            alert('workorder project name null');
        };
    }
});




$("body").on('click', '#downworkorder', function(){
    var applicationtime = $(this).attr('time')
    if (confirm('请确认关闭工单')) {
        var param = {
            applicationtime: applicationtime
        }
        $.post('/update_workorder', param, function(data){
            alert(data.status+"  "+data.log);
            waitworkorder();

        }, 'json');
    };
});




$("body").on('click', '.statistics', function(){
    var menu = $(this).attr('menu');
    if(menu == 'portlist'){
        postlist()
    } else if(menu == 'projectlist'){
        projectall()
    } else if(menu == 'hostlisterr'){
        hostlisterrweb()
    } else if(menu == 'onlinenum'){
        online_statistics()
    }
});

$("body").on('click', '.hostmanage', function(){
    $('#create_hosts_result').html("");
    $('#ProgressBarDiv').html("");
    var menu = $(this).attr('menu');
    if(menu == 'createhost'){
        createhost()
    } else if(menu == 'hostmanagelist'){
        hostmanagelist()
    } 
});


function createhost(){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>创建主机</th><th>选择</th><th>备注</th></tr>');
            htm.push('<tr>');
            htm.push('<td>业务线</td>');
            htm.push('<td>'+'<select class="form-control" id="selectbiggroup" onchange="get_area()"><option value="pp-online">皮皮线上</option><option value="pp-test">皮皮测试</option><option value="zy-online">最右线上</option><option value="zy-test">最右测试</option><option value="hanabi-online">火花线上</option><option value="hanabi-test">火花测试</option></select>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>可用区</td>');
            htm.push('<td>'+'<div id="area" class="sidebar-menu"> </div>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>配置</td>');
            htm.push('<td>'+'<div id="configuration" class="sidebar-menu"> </div>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>镜像</td>');
            htm.push('<td>'+'<select class="form-control" id="selectimage"><option value="centos7-zy1">centos7-zy1</option><option value="centos7-db1">centos7-db1</option><option value="centos7-ffmpeg">centos7-ffmpeg</option></select>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>主机名</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="hostnames" placeholder="多台主机,空格分割主机名" value="">'+'</td>');
            htm.push('<td>多台空格分割</td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td></td>');
            htm.push('<td>'+'<button id="create_hosts" class="btn btn-small btn-success" >创建主机实例</button>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
        $('#hostmanage').html(htm.join(''));

    get_area()
};

function hostmanagelist(){

    $.getJSON('/hostlistall', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>hostname</th><th>ip</th><th>实例id</th><th>配置</th><th>重新初始化</th><th>修改主机名</th><th>关机注销</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+'重新初始化'+'</td>');
            htm.push('<td>'+'修改主机名'+'</td>');
            htm.push('<td>'+'关机注销'+'</td>');
            htm.push('</tr>');
        }
        $('#hostmanage').html(htm.join(''));
    });
};

function get_area(){
    var selectbiggroup = $('#selectbiggroup').val()
    var param = {
        biggroup: selectbiggroup
    }
    $.getJSON('/get_area', param , function(data){

        var htm=['<select class="form-control" id="selectarea" onchange="get_configuration()">'];

        $.each(data, function(value, valuename){
            htm.push('<option value="'+value+'">'+valuename+'</option>');
        })
        htm.push('</select>');
        $('#area').html(htm.join(''));
        get_configuration()
    });
}


function get_configuration(){
    var selectarea = $('#selectarea').val()
    var param = {
        area: selectarea
    }
    $.getJSON('/get_configuration', param , function(data){

        var htm=['<select class="form-control" id="selectconfiguration">'];
        $.each(data, function(value, valuename){
            htm.push('<option value="'+value+'">'+valuename+'</option>');
        })
        htm.push('</select>');

        $('#configuration').html(htm.join(''));
    });
}


$("body").on('click', '#create_hosts', function(){
    $('#create_hosts_result').html("");
    $('#ProgressBarDiv').html("");
    var biggroup   = $('#selectbiggroup').val()
    var area   = $('#selectarea').val()
    var configuration   = $('#selectconfiguration').val()
    var image   = $('#selectimage').val()
    var hostnames   = $('#hostnames').val()

    if (confirm('请确认创建主机')) {
        var param = {
            biggroup: biggroup,
            area: area,
            configuration: configuration,
            image: image,
            hostnames: hostnames,
        }
        $.post('/create_hosts', param, function(data){
            alert(data.status+"  "+data.log);
            if(data.status == 'ok'){
                if(timeout2){clearInterval(timeout2)};
                timeout2 = setInterval(function(){
                    get_create_hosts_result(data.create_hosts_taskid);
                },2000);
                //$('#create_hosts_result').html("");
                //$('#ProgressBarDiv').html("");
            } else {
                alert(data.status + ' 失败 ' + data.log)
            };
        }, 'json');
    };
});



function get_create_hosts_result(create_hosts_taskid){
    var param={ taskid: create_hosts_taskid };
    $.getJSON('/get_create_hosts_result', param,  function(data){

        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>主机</th><th>任务id</th><th>状态</th><th>执行过程</th></tr>');
        if(data.status == 'ok'){
            var percentage=100;
            var ProgressBarStatus='progress-bar-success';
            clearInterval(timeout2);
            htm.push('<tr>');
            htm.push('<td class="success">'+data.hostnames+'</td>');
            htm.push('<td class="success">'+data.taskid+'</td>');
            htm.push('<td class="success">'+data.status+'</td>');
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data.log+'</textarea></td>');
            htm.push('</tr>');
        }  else if(data.status == 'wait') {
            var percentage=50;
            var ProgressBarStatus='progress-bar-success';
        } else if(data.status == 'fail') {
            var percentage=60;
            var ProgressBarStatus='progress-bar-danger';
            clearInterval(timeout2);
            htm.push('<tr>');
            htm.push('<td class="danger">'+data.hostnames+'</td>');
            htm.push('<td class="danger">'+data.taskid+'</td>');
            htm.push('<td class="danger">'+data.status+'</td>');
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data.log+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');

        $('#create_hosts_result').html(htm.join(''));

        var ProgressBar='<div class="progress-bar '+ProgressBarStatus+' progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';
        $('#ProgressBarDiv').html(ProgressBar);

    });
};
