(require '[clojure.string :as st])

(defn _split-space
  "split at spaces"
  [sentence]
  (st/split sentence #"\s"))

(defn sents-to-corpus
  [sents]
  (for [[es fs] sents]
    [(_split-space es) (_split-space fs)]))

(defn corpus
  "convert from sentences to corpus"
  [sents]
  (sents-to-corpus sents))

(defn f-words
  [corpus]
  (set
    (reduce into (for [[_ fs] corpus] fs))))

(def sents [["the house", "das Haus"]
            ["the book", "das Buch"]
            ["a book", "ein Buch"]])





