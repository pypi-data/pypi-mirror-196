/*******************************************************************************
* Copyright 2022 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#ifndef COMMON_PRIMITIVE_DESC_IFACE_HPP
#define COMMON_PRIMITIVE_DESC_IFACE_HPP

#include "oneapi/dnnl/dnnl.h"

#include "c_types_map.hpp"
#include "cache_blob.hpp"

// dnnl_primitive_desc is a user facing entity that has an alias
// primitive_desc_iface_t for internal use.
// The primitive_desc_iface_t is responsible for holding:
// 1. impl::primitive_desc_t - a primitive descriptor implementation that
// can be stored in the primitive cache as part of the primitive implementation
// to which it belongs
// 2. engine_t - a dnnl engine
struct dnnl_primitive_desc : public dnnl::impl::c_compatible {
    dnnl_primitive_desc(const std::shared_ptr<dnnl::impl::primitive_desc_t> &pd,
            dnnl::impl::engine_t *engine);

    virtual ~dnnl_primitive_desc() = default;

    const char *info() const;
    dnnl::impl::engine_t *engine() const;
    const dnnl::impl::primitive_attr_t *attr() const;
    virtual dnnl::impl::engine_t *scratchpad_engine() const;

    virtual dnnl::impl::engine_t *src_engine() const;
    virtual dnnl::impl::engine_t *dst_engine() const;

    virtual dnnl::impl::status_t query(
            dnnl::impl::query_t what, int idx, void *result) const;

    virtual dnnl::impl::status_t create_primitive_iface(
            std::pair<primitive_iface_t *, bool> &primitive_iface,
            const dnnl::impl::cache_blob_t &cache_blob) const;

    const std::shared_ptr<dnnl::impl::primitive_desc_t> &impl() const;

protected:
    std::shared_ptr<dnnl::impl::primitive_desc_t> pd_;
    dnnl::impl::engine_t *engine_;
};

#endif
