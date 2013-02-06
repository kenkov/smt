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

(defn s-total-func
  [es fs t initial-val]
  (let
    [foreign-es (into [] (set es))]
    (let [mp (into [] (map #(vector % (t % initial-val)) (for [e foreign-es f fs] [e f])))]
      (reduce
        (fn [_mp [[e f] vl]] (conj _mp [e (+ (_mp e 0) vl)]))
        {}
        mp))))

(defn count-func
  [es fs t s-total initial-val]
  (let [mp (into [] (map #(vector % (t % initial-val)) (for [e es f fs] [e f])))]
    (reduce
      (fn [_mp [[e f] vl]]
        (conj _mp [[e f] (+ (_mp [e f] 0)
                            (/ (t [e f] initial-val) (s-total e)))]))
      {}
      mp)))

(defn total-func
  [es fs t s-total initial-val]
  (let [mp (into [] (map #(vector % (t % initial-val)) (for [e es f fs] [e f])))]
    (reduce
      (fn [_mp [[e f] vl]]
        (conj _mp [f (+ (_mp f 0)
                        (/ (t [e f] initial-val) (s-total e)))]))
      {}
      mp)))

(defn _count-total
  [es fs t initial-val]
  (let
    [s-total-map (s-total-func es fs t initial-val)
     count-map (count-func es fs t s-total-map initial-val)]
    [s-total-map count-map]))

(defn count-total
  [corpus t initial-val]
  (let
    [mp (map (fn [[es fs]] (_count-total es fs t initial-val)) corpus)]
    (reduce
      (fn [[[s-total-map count-map]] [_s-total-map _count-map]]
        [(into s-total-map _s-total-map)
         (into count-map _count-map)])
      []
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
(def stotal (s-total-func es fs t 0))

(def count-map (count-func es fs {} stotal 1))
(def total-map (total-func es fs t stotal))
(def sents [["the house", "das Haus"]
            ["the book", "das Buch"]
            ["a book", "ein Buch"]])
(def corpus (sents-to-corpus sents))
(estimate count-map total-map)
(_count-total es fs {} 1)
(count-total corpus {} 1)

