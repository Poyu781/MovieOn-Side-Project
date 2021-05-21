const itemsSection = document.querySelector(".itemsSection");
function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie");
    node.setAttribute("id", movieObject.imdb.imdb_id)
    let img = movieObject.imdb.image;
    let title = movieObject.imdb.movie_title;
    let imdb_rating = movieObject.imdb_rating
    let rotten_audience_rating = movieObject.audience_rating
    let rotten_tomator_rating = movieObject.tomator_rating
    let douban_rating = movieObject.douban_rating
    let htmlText = `
  <img src=${img}>
  <div class="information">
    <div class="productInfo">
      <div>${title}</div>
      <div>IMDb:${imdb_rating}</div>
      <div>Rotten Audience:${rotten_audience_rating}</div>
      <div>Rotten Reviewer:${rotten_tomator_rating}</div>
      <div>Douban :${douban_rating}</div>
    </div>
  </div>
  `;
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
}


function main(url,offsetNum) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist["results"]; //I will get a list of dict
            console.log(dataArray)
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            if (offsetNum == 0){
                let node = document.createElement("div");
                node.classList.add("itemsWrap");
                // node.setAttribute("id", `wrap${row}`);
                itemsSection.appendChild(node);
            }
            itemsWrap = document.querySelector('.itemsWrap');
            for (let i = 0; i < num; i++) {

                try {
                    renderMovies(dataArray[i], itemsWrap);
                } catch {
                    let node = document.createElement("div");
                    node.classList.add("item");
                    itemsWrap.appendChild(node);
                }
            }

        });
}
offsetNum = 0
main('/api/rating/?limit=12&offset=0',offsetNum)

showMoreButton = document.querySelector(".showMore")
showMoreButton.addEventListener("click",()=>{
    offsetNum += 12
    main(`/api/rating/?limit=12&offset=${offsetNum}`,offsetNum)
})