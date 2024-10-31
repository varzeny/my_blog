// post.js
'use strict';

document.addEventListener("DOMContentLoaded", init);

const MODAL = {
    delete:null,
    init:function(){
        this.delete = document.getElementById("modal-delete");

        let btn_x = document.getElementById("btn-modal-x");
        btn_x.addEventListener("click", ()=>{
            this.delete.style.display = "none";
        });
    }
}





const TAG = {
    comments:null,
    init:function(){
        this.comments = document.getElementsByClassName("comment");
        for(let cmt of this.comments){
            let btn_del = cmt.querySelector(".btn-delete");
            btn_del.addEventListener("click", (ev)=>{
                // 모달 등장
                MODAL.delete.style.top = `${ev.pageY}px`
                MODAL.delete.style.left = `${ev.pageX}px`
                MODAL.delete.style.display = "flex";

                // 모달에 코맨트 데이터 전달 id등
                MODAL.delete.querySelector("#comment_id").value = cmt.querySelector("#comment-id").value;
            });
        }
    }
}



function init(){
    // init
    MODAL.init();
    TAG.init();

}