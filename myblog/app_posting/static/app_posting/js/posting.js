// posting.js


document.addEventListener("DOMContentLoaded", init);

async function init() {
    
    // 이벤트


    console.log("posting.js 로드 완료");
}



async function get_post_by_slug(slug, page=1) {
    console.log("카테고리 또는 태그 눌림, slug : ", slug, "페이지 : ", page);
    try {
        const resp = await fetch(`/posting/posts/?slug=${slug}&page=${page}`);
        const respData = await resp.json();

        if (resp.ok) {
            // 포스트 목록을 담는 요소
            const postList = document.getElementById('post-list');
            postList.innerHTML = ''; // 기존 내용을 초기화

            respData.posts.forEach(post => {
                const a = document.createElement('a');
                a.href = `/posting/posts/${post.slug}`
                a.innerHTML = `
                <article>
                    <div class="left">
                        <img src="${post.thumbnail}" alt="${post.title} thumbnail">
                    </div>
                    <div class="right">
                        <h4>${post.title}</h4>
                        <p>${post.excerpt}</p>
                    </div>
                </article>
                `;
                postList.appendChild(a);
            });

            // 페이지네이션 업데이트
            updatePagination(slug, respData.page_number, respData.total_pages);
        } else {
            console.error("응답이 올바르지 않습니다.", respData);
        }
    } catch (e) {
        console.error("ERROR get_post_by_slug", e);
    }
}

function updatePagination(slug, currentPage, totalPages) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // 기존 페이지네이션 초기화

    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.innerText = 'Previous';
        prevButton.onclick = () => get_post_by_slug(slug, currentPage - 1);
        pagination.appendChild(prevButton);
    }

    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.innerText = 'Next';
        nextButton.onclick = () => get_post_by_slug(slug, currentPage + 1);
        pagination.appendChild(nextButton);
    }
}

