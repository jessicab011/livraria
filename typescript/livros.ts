
import {
  buscarLivro,
  cadastrarLivro,
  listarLivros,
  buscarLivrosPorTitulo,
} from "./catalogo.js";

console.log("Busca por título completo:", buscarLivro("Dom Casmurro"));

cadastrarLivro({
  id: 3,
  titulo: "Capitães da Areia",
  autor: "Jorge Amado",
  preco: 35.9,
  estoque: 8,
});

listarLivros();

console.log(
  "Busca parcial:",
  buscarLivrosPorTitulo("pequeno")
);
