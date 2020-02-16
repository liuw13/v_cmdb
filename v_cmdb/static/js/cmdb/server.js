 //打开页面，获取后端机房数据，生成动态option给到modal_rack.html
    $.ajax({
            type: 'GET',
            url: '/cmdb/api_idcs/',
            data: {},
            dataType: "json",
            success: function(result){
                data = result.data
                option='<option> </option>'
                $('#create_idc_id').append(option)
                for (idc of data){
                    option = '<option id=' + idc.id + '>' + idc.name + '</option>'
                    $('#create_idc_id').append(option)

                }
            },
            error: function(){

            },
         })

    $('#create_idc_id').change(function () {
        //idc_name=$(this).val()
        idc_id=$('#create_idc_id option:selected').attr('id')
        $.ajax({
            type: 'GET',
            url: '/cmdb/api_idcs/'+ idc_id,
            data: {},
            dataType: "json",
            success: function(result){
                $('#create_rack_id').empty()
                racks = result.racks
                for (rack of racks){
                    option = '<option id=' + rack.id + '>' + rack.name + '</option>'
                    $('#create_rack_id').append(option)
                }
            },
            error: function(){

            },
         })
    })
    //点击创建，弹出模态框
    $('#btn-create').click(function () {
        $('#create_modal').modal()

    })
    //点击模态框提交按钮，发送数据到后端
    $('#create_btn').click(function () {
        name = $('#create_name').val()
        rack_id=$('#create_rack_id option:selected').attr('id')
        sn = $('#create_sn').val()
        cpu = $('#create_cpu').val()
        memory = $('#create_memory').val()
        disk = $('#create_disk').val()
        ip = $('#create_ip').val()
        server_type = $('#create_server_type').val()
        status = $('#create_status').val()
        remark = $('#create_remark').val()
        data = {rack_id:rack_id,name:name,sn:sn,cpu:cpu,memory:memory,disk:disk,ip:ip,server_type:server_type,status:status,remark:remark}
        console.log(data)
        $.ajax({
            type: 'POST',
            url: '/cmdb/servers/',
            data: data,  // 前端传给后端的数据
            dataType: "json",
            success: function(result){
                console.log(result)
                location.reload()

            },
            error: function(){

            },
         })
    })
    //点击删除
    $('.btn_delete').click(function () {
        id = $(this).attr('obj-id')
        data = {}
        $.ajax({
            type: 'DELETE',
            url: '/cmdb/servers/'+id,
            data: data,  // 前端传给后端的数据
            dataType: "json",
            success: function(result){
                console.log(result)
                location.reload()

            },
            error: function(){

            },
         })
    })

    $('.btn-put').click(function () {
        $('#edit_modal').modal()
        id = $(this).attr('obj-id')

        $.ajax({
            type: 'GET',
            url: '/cmdb/api_racks/',
            data: {},
            dataType: "json",
            success: function(result){
                $('#edit_racks_id').empty()
                data = result.data
                for (idc of data){
                    option = '<option id=' + racks.id + '>' + racks.name + '</option>'
                    $('#edit_rack_id').append(option)
                }
            },
            error: function(){

            },
         })

        $.ajax({
            type: 'GET',
            url: '/cmdb/api_servers/'+id,
            data: {},  // 前端传给后端的数据
            dataType: "json",
            success: function(result){
                console.log(result)
                rack_name = result.rack.name
                name = result.name
                sn = result.sn
                cpu = result.cpu
                memory = result.memory
                disk = result.disk
                ip = result.ip
                business = result.business
                server_type = result.server_type
                daq = result.daq
                status = result.status
                remark = result.remark
                $('#edit_rack_id').attr('value',rack_name)
                $('#edit_id').val(id)
                $('#edit_name').val(name)
                $('#edit_sn').val(sn)
                $('#edit_cpu').val(cpu)
                $('#edit_memory').val(memory)
                $('#edit_disk').val(disk)
                $('#edit_ip').val(ip)
                $('#edit_business').val(business)
                $('#edit_server_type').val(server_type)
                $('#edit_daq').val(daq)
                $('#edit_status').val(status)
                $('#edit_remark').val(remark)
            },
            error: function(){
            },
         })
    })

    $('#edit_btn').click(function () {
        name = $('#edit_name').val()
        sn = $('#edit_sn').val()
        cpu = $('#edit_cpu').val()
        memory = $('#edit_memory').val()
        disk = $('#edit_disk').val()
        ip = $('#edit_ip').val()
        business = $('#edit_business').val()
        server_type = $('#edit_server_type').val()
        daq = $('#edit_daq').val()
        status = $('#edit_status').val()
        remark = $('#edit_remark').val()
        id = $('#edit_id').val()
        rack_id = $('#edit_rack_id option:selected').attr('id')
        data = {rack_id:rack_id,name:name,sn:sn,cpu:cpu,memory:memory,disk:disk,ip:ip,business:business,server_type:server_type,daq:daq,status:status,remark:remark}

        $.ajax({
            type: 'PUT',
            url: '/cmdb/servers/'+id,
            data: data,  // 前端传给后端的数据
            dataType: "json",
            success: function(result){
                console.log(result)
                location.reload()

            },
            error: function(){

            },
         })
    })

    $('#search_btn').click(function () {
            var search = $('#search').val()
            window.location.href = "/cmdb/servers/?search=" + search
    })