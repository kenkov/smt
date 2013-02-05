(require '[clojure.string :as st])

(defn split-space
  "split at spaces"
  [sentence]
  (st/split sentence #"\s"))

(defn sents-to-corpus
  [sents]
  (for [[es fs] sents]
    [(split-space es) (split-space fs)]))

(defn corpus
  "convert from sentences to corpus"
  [sents]
  (sents-to-corpus sents))

(defn f-words
  [corpus]
  (set
    (reduce into (for [[_ fs] corpus] fs))))

(defn sum
  [lst]
  (reduce + 0 lst))

(defn count-keys
  [ky lst]
  (sum (map #(if (= % ky) 1 0) lst)))

(defn count-function
  [e f es fs t]
  (let
    [e-count (count-keys e es)
     f-count (count-keys f fs)
     t-sum (sum (for [_f fs] (t [e _f])))]
    (* (/ (t [e f]) t-sum) (* e-count f-count))))

(defn exist
  [ky lst]
  (some #{ky} lst))

;(defn count-dic
;  [corpus]
;  "define this function first"
;  (let [dic {}]
;    (for [[es fs] corpus]
;      (for [e es, f fs]
;        [into dic
;
;)

;(defn update
;  [e f t corpus]
;  (let
;    [numerator (sum (for [[es fs] corpus
;                          :when (and (exist e es)
;                                     (exist f fs))]
;                      (count-function e f es fs t)))
;     denominator

(def sents [["the house", "das Haus"]
            ["the book", "das Buch"]
            ["a book", "ein Buch"]])
