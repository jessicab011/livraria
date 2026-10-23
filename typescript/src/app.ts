import { livros } from "../catalogo.js";

const listaLivros = document.querySelector<HTMLDivElement>("#lista-livros");

if (!listaLivros) {
  throw new Error("Não foi possível encontrar a área do catálogo.");
}

for (const livro of livros) {
  const card = document.createElement("article");
  card.classList.add("card-livro");

  const titulo = document.createElement("h3");
  titulo.textContent = livro.titulo;

  const autor = document.createElement("p");
  autor.textContent = `Autor: ${livro.autor}`;

  const preco = document.createElement("p");
  preco.textContent = `Preço: ${livro.preco.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  })}`;

  const estoque = document.createElement("p");
  estoque.textContent = `Estoque: ${livro.estoque} unidades`;

  card.append(titulo, autor, preco, estoque);
  listaLivros.appendChild(card);
}