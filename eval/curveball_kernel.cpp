// Ordinary row-pair Curveball. Synthetic validation precedes real-data use.
// Build through curveball.py; no std::shuffle/uniform_int_distribution.
#include <algorithm>
#include <cstdint>
#include <exception>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {
thread_local std::string error;
struct Chain {
    std::vector<std::vector<uint32_t>> rows, initial;
    std::vector<uint32_t> common, pool;
    std::mt19937_64 rng;
    uint64_t attempts = 0, tradable = 0;
    uint32_t columns;

    Chain(uint64_t n, uint32_t c, const uint64_t* offsets,
          const uint32_t* labels, uint64_t seed) : rng(seed), columns(c) {
        if (offsets[0] != 0) throw std::invalid_argument("offsets must start at zero");
        rows.reserve(n);
        for (uint64_t i=0; i<n; ++i) {
            if (offsets[i+1] < offsets[i]) throw std::invalid_argument("offset order");
            rows.emplace_back(labels+offsets[i], labels+offsets[i+1]);
            const auto& row = rows.back();
            for (size_t j=0; j<row.size(); ++j) {
                if (row[j] >= c || (j && row[j-1] >= row[j]))
                    throw std::invalid_argument("rows must be sorted, unique and in range");
            }
        }
        initial = rows;
    }

    uint64_t bounded(uint64_t n) {
        if (!n) throw std::invalid_argument("empty random bound");
        const uint64_t threshold = -n % n;
        uint64_t value;
        do { value = rng(); } while (value < threshold);
        return value % n;
    }

    void step(uint64_t count) {
        if (rows.size() < 2) { attempts += count; return; }
        for (uint64_t t=0; t<count; ++t) {
            ++attempts;
            const size_t ia = bounded(rows.size());
            size_t ib = bounded(rows.size()-1);
            if (ib >= ia) ++ib;
            auto& a=rows[ia]; auto& b=rows[ib];
            common.clear(); pool.clear();
            size_t i=0, j=0, exclusive_a=0;
            while (i<a.size() || j<b.size()) {
                if (j==b.size() || (i<a.size() && a[i]<b[j])) {
                    pool.push_back(a[i++]); ++exclusive_a;
                } else if (i==a.size() || b[j]<a[i]) {
                    pool.push_back(b[j++]);
                } else { common.push_back(a[i]); ++i; ++j; }
            }
            // Failed row pairs remain self-loops in the chain.
            if (!exclusive_a || exclusive_a==pool.size()) continue;
            ++tradable;
            for (size_t k=pool.size(); k>1; --k)
                std::swap(pool[k-1], pool[bounded(k)]);
            a.assign(common.begin(), common.end());
            b.assign(common.begin(), common.end());
            a.insert(a.end(), pool.begin(), pool.begin()+exclusive_a);
            b.insert(b.end(), pool.begin()+exclusive_a, pool.end());
            std::sort(a.begin(), a.end()); std::sort(b.begin(), b.end());
        }
    }
};
}

extern "C" {
const char* cb_error() { return error.c_str(); }
void* cb_create(uint64_t n, uint32_t columns, const uint64_t* offsets,
                const uint32_t* labels, uint64_t seed) {
    try { return new Chain(n, columns, offsets, labels, seed); }
    catch (const std::exception& e) { error=e.what(); return nullptr; }
}
void cb_destroy(void* p) { delete static_cast<Chain*>(p); }
void cb_reference(void* p, const uint32_t* labels) {
    auto& chain=*static_cast<Chain*>(p);
    for (auto& row: chain.initial) for (auto& label: row) label=*labels++;
}
int cb_step(void* p, uint64_t attempts) {
    try { static_cast<Chain*>(p)->step(attempts); return 0; }
    catch (const std::exception& e) { error=e.what(); return -1; }
}
void cb_export(void* p, uint32_t* labels) {
    const auto& rows=static_cast<Chain*>(p)->rows;
    for (const auto& row: rows) for (auto label: row) *labels++=label;
}
void cb_margins(void* p, uint64_t* columns) {
    auto& chain=*static_cast<Chain*>(p);
    std::fill(columns, columns+chain.columns, 0);
    for (const auto& row: chain.rows) for (auto label: row) ++columns[label];
}
uint64_t cb_distance(void* p) {
    auto& chain=*static_cast<Chain*>(p);
    uint64_t distance=0;
    for (size_t k=0; k<chain.rows.size(); ++k) {
        const auto& a=chain.rows[k]; const auto& b=chain.initial[k];
        size_t i=0,j=0, shared=0;
        while (i<a.size() && j<b.size()) {
            if (a[i]<b[j]) ++i;
            else if (b[j]<a[i]) ++j;
            else { ++shared; ++i; ++j; }
        }
        distance += a.size()+b.size()-2*shared;
    }
    return distance;
}
uint64_t cb_attempts(void* p) { return static_cast<Chain*>(p)->attempts; }
uint64_t cb_tradable(void* p) { return static_cast<Chain*>(p)->tradable; }
int cb_counts(void* p, uint64_t n, const uint32_t* pairs, uint64_t* output) {
    try {
        auto& chain=*static_cast<Chain*>(p);
        std::unordered_map<uint64_t,size_t> index;
        index.reserve(n*2);
        std::fill(output, output+n, 0);
        for (size_t j=0;j<n;++j) {
            uint32_t a=pairs[2*j],b=pairs[2*j+1];
            if (a>=b || b>=chain.columns) throw std::invalid_argument("invalid eligible pair");
            uint64_t key=(uint64_t(a)<<32)|b;
            if (!index.emplace(key,j).second) throw std::invalid_argument("duplicate eligible pair");
        }
        for (const auto& row: chain.rows) {
            for (size_t i=0;i<row.size();++i) for(size_t j=i+1;j<row.size();++j) {
                auto found=index.find((uint64_t(row[i])<<32)|row[j]);
                if(found!=index.end()) ++output[found->second];
            }
        }
        return 0;
    } catch(const std::exception& e) { error=e.what(); return -1; }
}
}
