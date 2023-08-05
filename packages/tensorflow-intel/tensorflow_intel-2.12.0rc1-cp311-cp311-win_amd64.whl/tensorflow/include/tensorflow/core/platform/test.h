/* Copyright 2015 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_CORE_PLATFORM_TEST_H_
#define TENSORFLOW_CORE_PLATFORM_TEST_H_

#include <gtest/gtest.h>  // IWYU pragma: export
#include "tensorflow/core/platform/macros.h"
#include "tensorflow/core/platform/platform.h"
#include "tensorflow/core/platform/types.h"
#include "tensorflow/tsl/platform/test.h"

namespace tensorflow {

namespace testing {
using tsl::testing::PickUnusedPortOrDie;
using tsl::testing::RandomSeed;
using tsl::testing::TensorFlowSrcRoot;
using tsl::testing::TmpDir;

}  // namespace testing
}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_PLATFORM_TEST_H_
