/**
 * Created by Alex Korienev on 8/2/18.
 */
$(document).ready(function () {
   $.get('/student/collect-events/',function (events) {
       let event_block = $('#last-events')[0];
       let reports_checked_template = '<div class="alert alert-success" role="alert">Lab №{number} in course {shortened} was checked, mark is {mark}</div>';
       for (let i in events){
           if (events[i].category === "report-checked"){
               let event = events[i];
                event_block.innerHTML = event_block.innerHTML + reports_checked_template.
                    replace('{number}', event.report_num).replace('{shortened}', event.course).
                    replace('{mark}', event.mark)
           }
       }
   })
});