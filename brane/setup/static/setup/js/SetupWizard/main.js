import {
    AbstractDashboardApp
} from "/static/minerve/js/dashboards/DashboardApp/AbstractDashboardApp.js";

 export default class SetupWizard extends AbstractDashboardApp {
     settings = {
         "cidr": "#cidr",
         "pgpasswd": "#pgpasswd",
         "pgdata": "#pgdata",
         "ctrlport":"#ctrlport",
         "form":"#create_pod_form",
         "error": "#error_message",
         "progressbar": "#setup_pbar",
         "pcode":"#setup_code",


     }
     urls = {
         "_api_prefix":"/ws/api/v1/setup/",
         "install_exec":"create/start"
     }
     wsworker = false

     _on_success(res) {

     }
     _wsworker_data_handler(_res) {
         let res = JSON.parse(_res);
         // console.log("Websockets ",_res,res);
         if (res.type === "progress") {
                this.elements["progressbar"][0].style.width = res.prog+"%"
                this.elements["progressbar"][0].innerHTML = res.prog+"%"
                let statp = $("<span>",{"text":res.msg})
                this.elements["pcode"].append(statp,$("<br>"));
         } else if (res.type === "success") {
             this.elements["progressbar"][0].style.width = "100%"
             this.elements["progressbar"][0].innerHTML = res.msg
             this._on_success();
         } else if (res.type == "error") {

              this.elements["error"].text(res.step+" : "+res.msg);
              this.elements["error"].show();
              this.elements["progressbar"].parent().parent().hide();


         }
     }

     start() {
         this.showLoading();
         this.elements["error"] = $(this.settings["error"]);
         this.elements["form"] = $(this.settings["form"]);
         this.elements["progressbar"] = $(this.settings["progressbar"]);
         this.elements["pcode"] = $(this.settings["pcode"]);
         this.elements["error"] = $(this.settings["error"]);

         let cidr = $(this.settings.cidr)[0].value;
         let pgpasswd = $(this.settings.pgpasswd)[0].value;
         let pgdata = $(this.settings.pgdata)[0].value;
         let ctrlport = $(this.settings.ctrlport)[0].value;
         this.elements["error"].hide();
         this.wsworker = $.simpleWebSocket({
             url: this.urls["_api_prefix"]+this.urls["install_exec"],
         })
         this.wsworker.listen(this._wsworker_data_handler.bind(this));
         this.wsworker.connect();
         this.wsworker.send({
             "cmd":"create_cluster",
             "data":{
                 "cidr":cidr,
                 "pgpasswd":pgpasswd,
                 "pgdata":pgdata,
                 "ctrlport":ctrlport,
             }})

     }
     constructor(settings, urls, elements) {
        super();
    }
}