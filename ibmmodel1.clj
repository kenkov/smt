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

(defn s-total
  [es fs t]
  (let
    [foreign-es (into [] (set es))]
    (let [mp (into [] (map #(vector % (t %)) (for [e foreign-es f fs] [e f])))]
      (reduce
        (fn [_mp [[e f] vl]] (conj _mp [e (+ (_mp e 0) vl)]))
        {}
        mp))))

(defn count-func
  [es fs t s-total]
  (let [mp (into [] (map #(vector % (t %)) (for [e es f fs] [e f])))]
    (reduce
      (fn [_mp [[e f] vl]]
        (conj _mp [[e f] (+ (_mp [e f] 0)
                            (/ (t [e f]) (s-total e)))]))
      {}
      mp)))

(defn total-func
  [es fs t s-total]
  (let [mp (into [] (map #(vector % (t %)) (for [e es f fs] [e f])))]
    (reduce
      (fn [_mp [[e f] vl]]
        (conj _mp [f (+ (_mp f 0)
                        (/ (t [e f]) (s-total e)))]))
      {}
      mp)))

(defn estimate
  [count-map total-map]
  (reduce
    (fn [_mp [[e f] vl]]
      (conj _mp [[e f] (/ (count-map [e f]) (total-map f))]))
    {}
    count-map))

; tests
(def es [1 2 1])
(def fs [4 5 4])
(def t {[1 4] 1, [1 5] 2, [2 4] 3, [2 5] 4})
(def stotal (s-total es fs t))

(s-total es fs t)
(def count-map (count-func es fs t stotal))
(def total-map (total-func es fs t stotal))
(estimate count-map total-map)

(def sents [["the house", "das Haus"]
            ["the book", "das Buch"]
            ["a book", "ein Buch"]])
